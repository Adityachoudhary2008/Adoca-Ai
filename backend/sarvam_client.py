import numpy as np
from typing import List, Optional
import requests
from backend.config import settings
from backend.logger import logger


class SarvamAIClient:
    """Client for Sarvam AI API - embeddings and responses.

    Tries to use the official `sarvamai` SDK when available, otherwise falls
    back to plain HTTP requests. Logs full tried URLs and server responses
    to aid debugging (useful for deployed environments).
    """

    def __init__(self):
        self.api_key: str = settings.SARVAM_API_KEY
        self.api_base: str = settings.SARVAM_API_BASE.rstrip("/")
        self.embedding_model: str = settings.SARVAM_EMBEDDING_MODEL
        self.response_model: str = settings.SARVAM_RESPONSE_MODEL

        if not self.api_key:
            raise ValueError("SARVAM_API_KEY not configured in .env")

        # Optional SDK client
        self._sdk = None
        try:
            import sarvamai

            try:
                self._sdk = sarvamai.SarvamAI(api_subscription_key=self.api_key)
                logger.info("sarvamai SDK initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize sarvamai SDK: {e}")
                self._sdk = None
        except Exception:
            self._sdk = None

    def _http_post(self, path: str, payload: dict, timeout: int = 30) -> Optional[requests.Response]:
        url = f"{self.api_base}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        logger.info(f"POST {url} (model={payload.get('model')})")
        logger.debug(f"Payload (truncated): {str(payload)[:1000]}")
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=timeout)
            logger.debug(f"Response [{r.status_code}] (truncated): {r.text[:1000]}")
            return r
        except Exception as e:
            logger.error(f"HTTP POST failed for {url}: {e}")
            return None

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Return normalized embedding vector for input text, or None on error."""
        try:
            # SDK path
            if self._sdk is not None:
                try:
                    resp = self._sdk.embeddings.create(model=self.embedding_model, input=text)
                    # Try to parse common SDK shapes
                    if isinstance(resp, dict):
                        emb = resp.get("data", [{}])[0].get("embedding")
                    else:
                        emb = getattr(getattr(resp, 'data', [None])[0], 'embedding', None)
                    if not emb:
                        logger.error(f"SDK returned no embedding: {str(resp)[:1000]}")
                        return None
                except Exception as e:
                    logger.error(f"SDK embedding call failed: {e}")
                    return None
            else:
                # Try /v1 then fallback to non-versioned path
                payload = {"model": self.embedding_model, "input": text}
                tried = []
                for path in ["/v1/embeddings", "/embeddings"]:
                    tried.append(f"{self.api_base}{path}")
                    r = self._http_post(path, payload, timeout=10)
                    if r is None:
                        continue
                    if r.status_code == 404:
                        logger.warning(f"Endpoint returned 404: {r.request.url}")
                        continue
                    if r.status_code != 200:
                        logger.error(f"Embedding API error: {r.status_code} - {r.text} | tried: {tried}")
                        return None
                    data = r.json()
                    emb = data.get("data", [{}])[0].get("embedding")
                    break

            # Normalize
            import numpy as _np

            emb_arr = _np.array(emb, dtype=float)
            norm = _np.linalg.norm(emb_arr)
            if norm > 0:
                emb_arr = emb_arr / norm
            return emb_arr.tolist()
        except Exception as e:
            logger.error(f"Failed to get embedding: {e}")
            return None

    def get_response(self, system_prompt: str, user_message: str, context: str) -> Optional[str]:
        """Return LLM response string or None on error."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuery: {user_message}"},
            ]

            if self._sdk is not None:
                try:
                    resp = None
                    # Try common SDK method patterns
                    try:
                        resp = self._sdk.chat.completions.create(model=self.response_model, messages=messages,
                                                                 max_tokens=settings.MAX_RESPONSE_LENGTH,
                                                                 temperature=0.3)
                    except Exception:
                        resp = self._sdk.completions.create(model=self.response_model, messages=messages,
                                                             max_tokens=settings.MAX_RESPONSE_LENGTH,
                                                             temperature=0.3)

                    if isinstance(resp, dict):
                        msg = resp.get('choices', [{}])[0].get('message', {}).get('content', '')
                    else:
                        # Attempt attribute access
                        msg = None
                        try:
                            msg = resp.choices[0].message.content
                        except Exception:
                            msg = None
                    if not msg:
                        logger.error(f"SDK chat response malformed: {str(resp)[:1000]}")
                        return None
                    return msg.strip()
                except Exception as e:
                    logger.error(f"SDK chat call failed: {e}")
                    return None

            # HTTP fallback
            payload = {
                "model": self.response_model,
                "messages": messages,
                "max_tokens": settings.MAX_RESPONSE_LENGTH,
                "temperature": 0.3,
            }
            tried = []
            for path in ["/v1/chat/completions", "/chat/completions"]:
                tried.append(f"{self.api_base}{path}")
                r = self._http_post(path, payload, timeout=30)
                if r is None:
                    continue
                if r.status_code == 404:
                    logger.warning(f"Chat endpoint returned 404: {r.request.url}")
                    continue
                if r.status_code != 200:
                    logger.error(f"Response API error: {r.status_code} - {r.text} | tried: {tried}")
                    return None
                data = r.json()
                msg = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return msg.strip()

        except Exception as e:
            logger.error(f"Failed to get response: {e}")
            return None

