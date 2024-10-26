def html_content_username_password(username: str, password: str):
    html_content = f"""
                    <html>
                        <head>
                            <style>
                                .email-container {{
                                    background-color: #f3f4f6;
                                    padding: 20px;
                                    font-family: Arial, sans-serif;
                                }}
                                .email-header {{
                                    background-color: #4CAF50;
                                    color: white;
                                    padding: 10px;
                                    text-align: center;
                                    font-size: 24px;
                                }}
                                .email-body {{
                                    background-color: white;
                                    padding: 20px;
                                    margin-top: 10px;
                                    border-radius: 8px;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                .otp-code {{
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: #4CAF50;
                                    text-align: center;
                                    margin-top: 20px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="email-header">
                                    Kandy LMS
                                </div>
                                <div class="email-body">
                                    <p><b>Dear,</b></p>
                                    <div class="otp-code">Username: {username}</div><br/>
                                    <div class="otp-code">Password: {password}</div>
                                </div>
                            </div>
                        </body>
                    </html>
                    """
    return html_content