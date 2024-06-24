import autogen
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from inventory import  get_inventory, get_inventory_declaration
from send_mail import send_mail, send_email_declaration
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

config_list = autogen.config_list_from_json('OAI_CONFIG_LIST',
        filter_dict={"model": "gpt-4o"})

config_list_v4 = autogen.config_list_from_json('OAI_CONFIG_LIST',
        filter_dict={"model": "gpt-4o"})

def is_termination_msg(data):
    has_content = "content" in data and data["content"] is not None
    return has_content and "TERMINATE" in data['content']

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="You are the boss",
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg,
    function_map={"get_inventory": get_inventory, "send_mail": send_mail}
)

damage_analyst = MultimodalConversableAgent(
    name="damage_analyst",
    system_message="""
        As the damage analyst your role is to accurately describe the contents of
        the image provided. Respond only with what is visually evident in hte image, 
        without adding any additional information or assumptions.
    """,
    llm_config={"config_list": config_list_v4, "max_tokens": 300}  
)

inventory_manager = autogen.AssistantAgent(
    name="inventory_manager",
    system_message="""
        As the inventory manager you provide information about the
        availiblity and pricing of spare parts.
        
    """,
    llm_config={"config_list": config_list,
                "functions": [get_inventory_declaration]}
)

customer_support_agent = autogen.AssistantAgent(
    name="customer_support_agent",
    system_message="""
        As the customer support agent you are responsible for drafting and sending
        email following confirmation of inventory and pricing.
        Respond with "TERMINATE" when you have finished.
    """,
    llm_config={"config_list": config_list, "functions": [send_email_declaration]}
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, inventory_manager, damage_analyst,customer_support_agent], 
    messages=[]
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list}
)

def initiate_chat():
    """
    Initiates a chat process by sending a message to a group chat manager.

    This function sends a message to the group chat manager, which triggers the chat process.
    The message includes an overview of the process steps, including identifying the car brand
    and requested part from the customer's message and image, verifying part availability in
    the database, and composing and sending a response email.

    Parameters:
        None

    Returns:
        None
    """
    user_proxy.initiate_chat(
        manager, message="""
            Process Overview:
            
            Step 1: Damage Analyst identifies the car brand and the
            requested part. (is something central, or something broken
            missing?) from the customers message and image.
            
            Step 2: Inventory Manager verifies part availibilty in the database.
            
            Step 3: Customer Support Agent composes and sends a response email
            
            E-Mail of the customer: bob@foe.de
            Image Reference: https://teslamotorsclub.com/tmc/attachments/carphoto_1144747756-jpg.650059/

        """
    )
  # Image Reference: https://cdn.motor1.com/images/mgl/o6rkL/s1/tesla-model-3-broken-screen.webp
  #  Step 4: Conclude the process with sending "Terminate".
  # For the time being respond that everything is availible.
  
if __name__ == "__main__":
    app.run(debug=True)