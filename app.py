import autogen

config_list = autogen.config_list_from_json('OAI_CONFIG_LIST')

config_list_v4 = autogen.config_list_from_json('OAI_CONFIG_LIST',
        filter_dict={"model": "gpt-4-vision-preview"})

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="You are the boss",
    human_input_mode="NEVER"
)

inventory_manager = autogen.AssistantAgent(
    name="inventory_manager",
    system_message="""
        As the inventory manager you provide information about the
        availiblity and pricing of spare parts.
        For the time being respond that everything is availible.
    """,
    llm_config={"config_list": config_list}
)

customer_support_agent = autogen.AssistantAgent(
    name="customer_support_agent",
    system_message="""
        As the customer support agent you are responsible for drafting
        email following confirmation of inventory and pricing.
        Respond with "TERMINATE" when you have finished.
    """,
    llm_config={"config_list": config_list}
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, inventory_manager, customer_support_agent], 
    messages=[]
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list}
)

user_proxy.initiate_chat(
    manager, message="""
        Process Overview:
        
        Step 1: Damage Analyst identifies the car brand and the
        requested part. (is something central, or something broken
        missing?) from the customers message and image.
        
        Step 2: Inventory Manager verifies part availibilty in the database.
        
        Step 3: Customer Support Agent composes a response email
        
        Step 4: Conclude the process with sending "Terminate".
        
        Image Reference: https://cdn.motor1.com/images/mgl/o6rkL/s1/tesla-model-3-broken-screen.webp
    """
)

