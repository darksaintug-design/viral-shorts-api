import stripe
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionService:
    """Handle Stripe subscription management"""
    
    @staticmethod
    def create_customer(email: str, customer_name: str = None) -> str:
        """
        Create a Stripe customer
        Returns: customer_id
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=customer_name or email
            )
            return customer.id
        except Exception as e:
            logger.error(f"Failed to create Stripe customer: {str(e)}")
            raise
    
    @staticmethod
    def create_subscription(customer_id: str, price_id: str) -> str:
        """
        Create a subscription
        Returns: subscription_id
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
            )
            return subscription.id
        except Exception as e:
            logger.error(f"Failed to create subscription: {str(e)}")
            raise
    
    @staticmethod
    def get_subscription(subscription_id: str):
        """
        Get subscription details
        """
        try:
            return stripe.Subscription.retrieve(subscription_id)
        except Exception as e:
            logger.error(f"Failed to retrieve subscription: {str(e)}")
            raise
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> bool:
        """
        Cancel a subscription
        """
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            logger.error(f"Failed to cancel subscription: {str(e)}")
            return False
