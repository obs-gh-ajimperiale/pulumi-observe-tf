import pulumi
import pulumi_observe as observe

config = pulumi.Config("observe")

observe_provider = observe.Provider("observe-provider",
    customer=config.require("customer"),
    domain=config.require("domain"),
    user_email=config.require_secret("user_email"),  # or use api_token instead
    user_password=config.require_secret("user_password") 
)
