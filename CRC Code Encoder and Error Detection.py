#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("CRC Encoder/Decoder")

        # Set window size
        self.setFixedSize(700, 300)

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create input widget and layout
        input_widget = QWidget()
        input_layout = QHBoxLayout()

        # Create message label and text box
        message_label = QLabel("Message (binary):")
        self.message_textbox = QLineEdit()

        # Create received message label and text box
        received_message_label = QLabel("Received Message (binary):")
        self.received_message_textbox = QLineEdit()

        # Create divisor label and text box
        divisor_label = QLabel("Divisor (binary):")
        self.divisor_textbox = QLineEdit()

        # Add input widgets to layout
        input_layout.addWidget(message_label)
        input_layout.addWidget(self.message_textbox)
        input_layout.addWidget(received_message_label)
        input_layout.addWidget(self.received_message_textbox)
        input_layout.addWidget(divisor_label)
        input_layout.addWidget(self.divisor_textbox)

        # Create encode and check buttons
        encode_button = QPushButton("Encode")
        check_button = QPushButton("Check")

        # Connect buttons to corresponding functions
        encode_button.clicked.connect(self.encode_message)
        check_button.clicked.connect(self.check_message)

        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(encode_button)
        button_layout.addWidget(check_button)

        # Create output widget and layout
        output_widget = QWidget()
        output_layout = QVBoxLayout()

        # Create encoded message label and text box
        self.encoded_label = QLabel("Encoded Message (binary):")
        self.encoded_textbox = QLineEdit()
        self.encoded_textbox.setReadOnly(True)

        # Create error check label and text box
        self.error_label = QLabel("Error Check:")
        self.error_textbox = QLineEdit()
        self.error_textbox.setReadOnly(True)

        # Add output widgets to layout
        output_layout.addWidget(self.encoded_label)
        output_layout.addWidget(self.encoded_textbox)
        output_layout.addWidget(self.error_label)
        output_layout.addWidget(self.error_textbox)

        # Add input, button, and output layouts to main layout
        main_layout.addWidget(input_widget)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(output_widget)
        input_widget.setLayout(input_layout)
        output_widget.setLayout(output_layout)

        # Set main widget layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


    def encode_message(self):
        # Get input values from text boxes
        message = self.message_textbox.text()
        dm = message
        divisor = self.divisor_textbox.text()

        # Validate input values
        if not message:
            QMessageBox.warning(self, "Error", "Message field cannot be empty")
            return
        if not all(bit in ["0", "1"] for bit in message):
            QMessageBox.warning(self, "Error", "Message must be a binary string")
            return
        if not divisor:
            QMessageBox.warning(self, "Error", "Divisor field cannot be empty")
            return
        if not all(bit in ["0", "1"] for bit in divisor):
            QMessageBox.warning(self, "Error", "Divisor must be a binary string")
            return

        # Convert input values to binary lists
        message = [int(bit) for bit in message]
        divisor = [int(bit) for bit in divisor]

        # Append zeros to message for remainder
        message += [0] * (len(divisor) - 1)

        # Perform division using XOR operation
        for i in range(len(message)-len(divisor)+1):
            # If the leftmost bit of the message is 1, XOR the divisor with the message
            if message[i] == 1:
                for j in range(len(divisor)):
                    message[i+j] ^= divisor[j]

            # Convert binary encoded message back to string
#             encoded_message = "".join([str(bit) for bit in message])
            s2 = "".join(str(bit) for bit in message)
            s1 = "".join(str(i) for i in dm)
            l = (-1)*(len(divisor) - 1)
            output = s1 + s2[l:]

            # Set encoded message text box to display result
            self.encoded_textbox.setText(output)

    def check_message(self):
        # Get input values from text boxes
        received_message = self.received_message_textbox.text()
        divisor = self.divisor_textbox.text()

        # Validate input values
        if not received_message:
            QMessageBox.warning(self, "Error", "Message field cannot be empty")
            return
        if not all(bit in ["0", "1"] for bit in received_message):
            QMessageBox.warning(self, "Error", "Message must be a binary string")
            return
        if not divisor:
            QMessageBox.warning(self, "Error", "Divisor field cannot be empty")
            return
        if not all(bit in ["0", "1"] for bit in divisor):
            QMessageBox.warning(self, "Error", "Divisor must be a binary string")
            return

        # Convert input values to binary lists
        received_message = [int(bit) for bit in received_message]
        divisor = [int(bit) for bit in divisor]

        # Perform division using XOR operation
        for i in range(len(received_message)-len(divisor)+1):
            # If the leftmost bit of the message is 1, XOR the divisor with the message
            if received_message[i] == 1:
                for j in range(len(divisor)):
                    received_message[i+j] ^= divisor[j]

            # If the remainder is all zeros, the message is error-free
        if all(bit == 0 for bit in received_message[-len(divisor)+1:]):
            self.error_textbox.setText("No error detected")
        else:
            self.error_textbox.setText("Error detected")
            
            
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()


# 
