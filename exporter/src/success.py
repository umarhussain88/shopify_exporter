from helpers import toast_builder
import getpass



success = f"""
        <toast>
            <visual>
            <binding template='ToastGeneric'>
                <text>Installation Complete - Please Run Export File.vbs</text>
            </binding>
            </visual>
            <actions>
            <action
                content="Dismiss"
                arguments="action=dismiss"/>
            </actions>        
        </toast>
        """

if __name__ == '__main__':

    toast_builder(success)        