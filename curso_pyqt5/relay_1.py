import usb.core
import usb.util
import time

class VUSBDevice:
    def __init__(self, vendor_id, product_id):
        self.dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        
        if self.dev is None:
            raise ValueError('Device not found')
            
        # Set the active configuration
        self.dev.set_configuration()
        
    def send_command(self, data):
        try:
            # Control transfer example
            self.dev.ctrl_transfer(
                0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
                0x09,  # SET_CONFIGURATION
                0x300, # wValue
                0,     # wIndex
                data   # data to send
            )
            return True
        except usb.core.USBError as e:
            print(f"Error sending command: {e}")
            return False

# Usage example
def main():
    try:
        # Replace with your device's VID/PID
        device = VUSBDevice(vendor_id=0x16c0, product_id=0x05df)
        
        # Example command
        command_data = [0xff, 0x01, 0, 0, 0, 0, 0, 0]
        device.send_command(command_data)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()