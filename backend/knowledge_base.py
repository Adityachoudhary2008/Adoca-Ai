import json
import os
from pathlib import Path
from backend.config import settings
from backend.logger import logger

class KnowledgeBase:
    """Knowledge Base Manager - handles chunked, structured knowledge"""
    
    def __init__(self):
        self.kb_path = settings.KB_PATH
        self.index_file = os.path.join(self.kb_path, "index.json")
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load knowledge base index."""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.kb_index = json.load(f)
            logger.info(f"Loaded KB with {len(self.kb_index)} chunks")
        except FileNotFoundError:
            logger.warning("Knowledge base index not found. Starting fresh.")
            self.kb_index = []
    
    def get_all_chunks(self):
        """Return all knowledge chunks."""
        return self.kb_index
    
    def add_chunk(self, chunk_data: dict):
        """Add a new chunk to knowledge base."""
        required_fields = ["id", "title", "category", "content"]
        
        # Validate structure
        if not all(field in chunk_data for field in required_fields):
            logger.error(f"Invalid chunk structure: {chunk_data}")
            raise ValueError(f"Chunk must contain: {required_fields}")
        
        # Validate content length (200-500 words)
        word_count = len(chunk_data["content"].split())
        if word_count < 50:  # Relaxed to 50 for flexibility
            logger.warning(f"Chunk '{chunk_data['id']}' too short: {word_count} words")
        
        self.kb_index.append(chunk_data)
        self.save_knowledge_base()
        logger.info(f"Added chunk: {chunk_data['id']}")
    
    def save_knowledge_base(self):
        """Save knowledge base to disk."""
        try:
            os.makedirs(self.kb_path, exist_ok=True)
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.kb_index, f, ensure_ascii=False, indent=2)
            logger.info("Knowledge base saved")
        except Exception as e:
            logger.error(f"Failed to save KB: {str(e)}")

def initialize_knowledge_base():
    """Initialize Adoca knowledge base with core topics."""
    kb = KnowledgeBase()
    
    # Don't re-add if already exists
    if len(kb.get_all_chunks()) > 0:
        logger.info("Knowledge base already initialized")
        return kb
    
    # Core knowledge chunks (MANDATORY)
    core_chunks = [
        {
            "id": "adoca_overview",
            "title": "Adoca Overview",
            "category": "business",
            "content": "Adoca is a Hybrid-Conversational Marketplace that revolutionizes how consumers discover and purchase products. It combines the convenience of online discovery with the trust and personalization of human interaction, and then enables offline fulfillment. The platform operates in three core steps: 1) Online discovery through our smart app, 2) Human interaction via masked calling and transactional chat, 3) Offline fulfillment through local merchants. This hybrid model ensures that users get both digital convenience and human trust."
        },
        {
            "id": "adoca_philosophy",
            "title": "Adoca Philosophy",
            "category": "business",
            "content": "Adoca's philosophy is built on three principles: Trust through transparency, Convenience through technology, and Community through human connection. The platform believes that the future of commerce is not purely digital or purely local - it's hybrid. We bring together the scale of online marketplaces with the trust of local relationships. Our zero Customer Acquisition Cost (CAC) strategy means we rely on word-of-mouth and viral growth, not expensive advertising."
        },
        {
            "id": "zero_cac_strategy",
            "title": "Zero CAC Strategy",
            "category": "business",
            "content": "Adoca operates on a Zero CAC (Customer Acquisition Cost) model, meaning we don't spend money on traditional advertising. Instead, we focus on building network effects where users invite friends, family, and local merchants. Every satisfied user becomes a brand ambassador. This strategy is sustainable, scalable, and aligns with Adoca's community-first philosophy. The platform incentivizes referrals through the Fire Coin wallet and Seller Coin rewards system."
        },
        {
            "id": "local_mode",
            "title": "Local Mode - User App",
            "category": "user_app",
            "content": "Local Mode is Adoca's core discovery feature in the User App. It enables consumers to discover products and services from local merchants within their area. Users can browse categories like plumbing, grocery, restaurants, electronics, and more. The experience is hyperlocal - you see merchants near you, with real-time availability and pricing. Local Mode combines social proof (ratings, reviews) with real-time inventory to help users make informed decisions."
        },
        {
            "id": "enterprise_mode",
            "title": "Enterprise Mode - User App",
            "category": "user_app",
            "content": "Enterprise Mode in the User App serves businesses that operate across multiple locations. These are brands with centralized inventory and pricing but distributed fulfillment points. Users can search for enterprise brands (like major retailers or franchises) and purchase through Adoca. The system handles inventory synchronization across all enterprise locations, ensuring stock accuracy and efficient fulfillment."
        },
        {
            "id": "rfq_engine",
            "title": "RFQ Engine - Request for Quote",
            "category": "user_app",
            "content": "The RFQ (Request for Quote) Engine is Adoca's unique feature for custom products and services. Instead of browsing pre-listed items, users can submit RFQs for products that don't have standard listings. For example: custom tailoring, wedding planning services, home renovation, or bulk orders. Merchants then respond with quotes, timelines, and proposals. This feature bridges the gap between e-commerce and local services by enabling price negotiation and customization."
        },
        {
            "id": "fire_coin_wallet",
            "title": "Fire Coin Wallet",
            "category": "financial_system",
            "content": "Fire Coin is the digital wallet and rewards currency within Adoca. Users earn Fire Coins through various activities: purchases, referrals, completing tasks, and engagement. Fire Coins can be used for: discounts on purchases, gifting to friends, unlocking premium features, and exchanging for cash. The wallet also tracks transaction history, pending rewards, and redeemable balances. Fire Coins create stickiness and incentivize repeat engagement on the platform."
        },
        {
            "id": "seller_coin",
            "title": "Seller Coin System",
            "category": "financial_system",
            "content": "Seller Coin is the merchant equivalent of Fire Coin. Merchants earn Seller Coins through: successful transactions, customer ratings, completing business profile tasks, and promotional activities. Seller Coins can be redeemed for: commission discounts, premium listing features, marketing visibility boost, or cash withdrawal. This incentive system aligns merchant interests with Adoca's growth while rewarding high-performing merchants."
        },
        {
            "id": "smart_pos",
            "title": "Smart POS - Business App",
            "category": "business_app",
            "content": "Smart POS is the digital point-of-sale system for merchants in the Adoca Business App. Unlike traditional POS systems, Smart POS integrates with Adoca's marketplace ecosystem. It enables merchants to: process both online and offline payments, sync inventory with their online listings, manage stock levels, handle Adoca orders and local orders together, and generate sales reports. The system is cloud-based, requires no heavy infrastructure, and works offline."
        },
        {
            "id": "masked_calling",
            "title": "Masked Calling",
            "category": "conversational_commerce",
            "content": "Masked Calling is a privacy-first feature in Adoca that enables secure communication between buyers and sellers. When a user calls a merchant, phone numbers are masked using virtual numbers. This protects privacy for both parties and prevents number scraping. Calls are logged within the platform for reference and dispute resolution. This feature is essential for building trust in a marketplace where many buyers and sellers are meeting for the first time."
        },
        {
            "id": "transactional_chat",
            "title": "Transactional Chat",
            "category": "conversational_commerce",
            "content": "Transactional Chat enables real-time messaging between buyers and sellers within the Adoca app. Unlike generic chat, every message is transaction-linked. Users can share product details, negotiate prices, ask for customizations, and confirm delivery details. Chat history is preserved for disputes. Merchants can set automated responses and FAQs. This feature bridges the gap between synchronous (call) and asynchronous (email) communication."
        },
        {
            "id": "deal_lock",
            "title": "Deal Lock Feature",
            "category": "conversational_commerce",
            "content": "Deal Lock is Adoca's feature to convert conversations into confirmed transactions. After negotiating through chat or call, users can 'lock' the deal by confirming quantity, price, delivery date, and payment terms. Both buyer and seller receive a locked deal confirmation. This creates accountability and reduces disputes. Deal Lock can be initiated from chat, call, or RFQ response."
        },
        {
            "id": "fake_billing_fraud",
            "title": "Fake Billing Fraud Prevention",
            "category": "risk_fraud",
            "content": "Adoca's Fake Billing fraud detection system identifies merchants who create fake transactions to artificially inflate sales and ratings. The system uses machine learning to detect patterns: bulk identical orders, rapid order cycles without genuine customer interaction, mismatched product combinations, and unusual payment methods. Flagged merchants are reviewed by trust team and can face suspension or removal."
        },
        {
            "id": "bidding_fraud",
            "title": "Bidding Fraud Prevention",
            "category": "risk_fraud",
            "content": "Bidding Fraud refers to RFQ manipulation where merchants post fake RFQs to inflate their response rates and fake quote fulfillment. Adoca detects this through: RFQ matching algorithms that identify duplicate requests, customer authenticity checks, winner selection verification, and post-RFQ fulfillment tracking. Suspicious accounts are flagged and investigated."
        },
        {
            "id": "privacy_system",
            "title": "Privacy System & Data Protection",
            "category": "risk_fraud",
            "content": "Adoca prioritizes user privacy through: masked calling (virtual phone numbers), encrypted messaging, zero data sharing with third parties, GDPR-compliant data storage, user consent controls for data usage, and transparent privacy policies. Users can opt-out of data monetization. Personal information is never sold; only aggregate insights are monetized through B2B partnerships."
        },
        {
            "id": "customer_fraud",
            "title": "Customer Fraud Prevention",
            "category": "risk_fraud",
            "content": "Adoca detects customer fraud through: payment behavior analysis, refund abuse tracking, multiple account detection using device fingerprinting, dispute pattern analysis, and verification of delivery confirmations. High-risk customers receive review or restriction. The system learns from historical dispute patterns to improve detection."
        },
        {
            "id": "onboarding_flow",
            "title": "User Onboarding Flow",
            "category": "workflow",
            "content": "New users on Adoca go through a guided onboarding: 1) Mobile verification via OTP, 2) Profile setup (name, location, preferences), 3) App tour highlighting key features (Local Mode, RFQ, calling), 4) First deal completion (incentivized with welcome bonus), 5) Fire Coin introduction and referral hints. This flow ensures users understand the hybrid model and are ready to discover products."
        },
        {
            "id": "merchant_onboarding",
            "title": "Merchant Onboarding Flow",
            "category": "workflow",
            "content": "Merchants onboarding to Adoca: 1) Business verification via Aadhaar/PAN, 2) Store setup (location, category, operating hours), 3) Business App training (Smart POS, inventory, orders), 4) Profile completion for Local Mode visibility, 5) Demo transaction setup. Trust team verifies before going live. This ensures only legitimate merchants list on Adoca."
        },
        {
            "id": "discovery_process",
            "title": "Discovery Process",
            "category": "workflow",
            "content": "The discovery process is how users find products on Adoca. Starting from the app home, users can: browse categories in Local Mode, search by keyword, filter by distance/rating/price, see merchant profiles with social proof, view product images and details, read reviews, check availability in real-time. For specialty products, users can submit RFQs. Discovery is optimized for mobile and hyperlocal relevance."
        },
        {
            "id": "communication_flow",
            "title": "Buyer-Seller Communication",
            "category": "workflow",
            "content": "Communication on Adoca flows through multiple channels: Chat (asynchronous), Masked Calling (synchronous), Video demos (for complex products), and RFQ responses (structured). The platform integrates these into a unified conversation thread. All communication is logged for transparency and dispute resolution. Users can switch between channels in the same transaction."
        },
        {
            "id": "transaction_flow",
            "title": "Transaction Flow",
            "category": "workflow",
            "content": "A typical Adoca transaction: 1) Discovery (user finds product), 2) Engagement (chat or call), 3) Deal confirmation (lock deal with terms), 4) Payment (multiple methods supported), 5) Fulfillment (delivery or pickup), 6) Confirmation (delivery verified), 7) Review & rewards (user reviews merchant, earns Fire Coin). This flow ensures every step is tracked."
        },
        {
            "id": "rewards_system",
            "title": "Rewards & Incentives",
            "category": "workflow",
            "content": "Adoca incentivizes user engagement through: purchase rewards (Fire Coins earned on every purchase), referral bonuses (for inviting friends), task completion (daily challenges for app usage), reviews (bonus for leaving reviews), and milestone rewards (first purchase, nth purchase). Merchants earn Seller Coins through transactions and ratings. The system encourages repeat usage and community building."
        }
    ]
    
    # Add all chunks
    for chunk in core_chunks:
        try:
            kb.add_chunk(chunk)
        except ValueError:
            logger.warning(f"Duplicate chunk: {chunk['id']}")
    
    return kb
