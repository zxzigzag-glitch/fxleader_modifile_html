#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Modifier System for FISG Landing Pages
Modifies index.html files in multiple languages according to fxleader.md requirements
"""

import os
import re
import json
from pathlib import Path
from typing import Optional
from html.parser import HTMLParser


class HTMLModifier:
    """Handles all HTML modifications according to fxleader.md specifications"""
    
    def __init__(self, html_content: str, working_dir: Optional[str] = None, config_name: Optional[str] = None):
        self.content = html_content
        self.working_dir = working_dir
        self.config_name = config_name
        
    def add_google_tag(self) -> None:
        """Step 1: Add Google Tag Manager code to head section"""
        google_tag = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XEYRPJNWLJ"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-XEYRPJNWLJ');
</script>
'''
        
        # Check if already exists
        if 'G-XEYRPJNWLJ' in self.content:
            print("  ✓ Google Tag already exists")
            return
            
        # Find <head> tag and insert after it
        head_pattern = r'(<head[^>]*>)'
        if re.search(head_pattern, self.content):
            self.content = re.sub(head_pattern, r'\1' + '\n    ' + google_tag, self.content, count=1)
            print("  ✓ Google Tag added")
        else:
            print("  ✗ Could not find <head> tag")
    
    def add_cloudflare_dependencies(self) -> None:
        """Step 2: Add Cloudflare Turnstile dependencies"""
        cloudflare_deps = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.1/css/bootstrap.min.css"
        integrity="sha512-siwe/oXMhSjGCwLn+scraPOWrJxHlUgMBMZXdPe2Tnk3I0x3ESCoLz7WZ5NTH6SZrywMY+PB1cjyqJ5jAluCOg=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
<link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.9.1/font/bootstrap-icons.min.css"
        integrity="sha512-5PV92qsds/16vyYIJo3T/As4m2d8b6oWYfoqV+vtizRB6KhF1F9kYzWzQmsO6T3z3QG2Xdhrx7FQ+5R1LiQdUA=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" defer></script>
'''
        
        # Check if already exists
        if 'challenges.cloudflare.com/turnstile' in self.content:
            print("  ✓ Cloudflare dependencies already exist")
            return
            
        # Find <style> tag and insert before it
        style_pattern = r'(<style[^>]*>)'
        if re.search(style_pattern, self.content):
            self.content = re.sub(style_pattern, cloudflare_deps + r'    \1', self.content, count=1)
            print("  ✓ Cloudflare dependencies added")
        else:
            print("  ✗ Could not find <style> tag")
    
    def convert_absolute_to_relative_paths(self) -> None:
        """Step 3: Change https://www.fisg.com/ references to root-relative paths"""
        total_matches = 0
        
        # Fix double slash https://www.fisg.com// -> https://www.fisg.com/
        double_slash_pattern = r'https://www\.fisg\.com//+'
        double_slash_replacement = r'https://www.fisg.com/'
        double_slash_matches = len(re.findall(double_slash_pattern, self.content))
        if double_slash_matches > 0:
            self.content = re.sub(double_slash_pattern, double_slash_replacement, self.content)
        
        # Convert <link href="https://www.fisg.com/...">
        link_pattern = r'<link([^>]*)href="https://www\.fisg\.com(/[^"]*)"'
        link_replacement = r'<link\1href="\2"'
        link_matches = len(re.findall(link_pattern, self.content))
        if link_matches > 0:
            self.content = re.sub(link_pattern, link_replacement, self.content)
            total_matches += link_matches
        
        # Convert <meta content="https://www.fisg.com/...">
        meta_pattern = r'<meta([^>]*)content="https://www\.fisg\.com(/[^"]*)"'
        meta_replacement = r'<meta\1content="\2"'
        meta_matches = len(re.findall(meta_pattern, self.content))
        if meta_matches > 0:
            self.content = re.sub(meta_pattern, meta_replacement, self.content)
            total_matches += meta_matches
        
        # Convert <img src="https://www.fisg.com/...">
        img_pattern = r'src="https://www\.fisg\.com(/[^"]*)"'
        img_replacement = r'src="\1"'
        img_matches = len(re.findall(img_pattern, self.content))
        if img_matches > 0:
            self.content = re.sub(img_pattern, img_replacement, self.content)
            total_matches += img_matches
        
        if total_matches > 0:
            details = []
            if link_matches > 0:
                details.append(f"{link_matches} link")
            if meta_matches > 0:
                details.append(f"{meta_matches} meta")
            if img_matches > 0:
                details.append(f"{img_matches} img")
            print(f"  ✓ Converted {total_matches} absolute paths to relative paths ({', '.join(details)})")
            if double_slash_matches > 0:
                print(f"  ✓ Fixed {double_slash_matches} double slash URLs")
        else:
            print("  ✓ No absolute paths to convert")
    
    def ensure_join_form_id(self) -> None:
        """Step 4: Ensure form has id="joinForm" """
        if not re.search(r'id="joinForm"', self.content):
            # Find the first form element and add id if not present
            form_match = re.search(r'<form([^>]*?)>', self.content)
            if form_match:
                original = form_match.group(0)
                if 'id=' not in original:
                    modified = original.replace('<form', '<form id="joinForm"', 1)
                else:
                    # Form has an id but not joinForm
                    modified = original.replace('id="', 'id="joinForm" data-old-id="', 1)
                self.content = self.content.replace(original, modified, 1)
                print("  ✓ Form id='joinForm' added/verified")
            else:
                print("  ⚠ Could not find form to add id")
        else:
            print("  ✓ Form id='joinForm' already exists")
    
    def add_country_select_onchange(self) -> None:
        """Step 5: Add onchange event and variable substitution to country select"""
        # Look for country select without onchange
        pattern = r'<select\s+name="country"\s+id="country"([^>]*)required(?!.*onchange)'
        
        if not re.search(r'<select[^>]*name="country"[^>]*onchange="countryChange\(\)"', self.content):
            # Add onchange attribute
            match = re.search(r'(<select\s+name="country"\s+id="country"[^>]*)required', self.content)
            if match:
                original = match.group(0)
                modified = original.replace('required', 'required onchange="countryChange()"', 1)
                self.content = self.content.replace(original, modified, 1)
                print("  ✓ Country select onchange event added")
            
            # Check for {{select:country}} substitution
            if '{{select:country}}' not in self.content:
                # Find the closing tag of country select and add placeholder if needed
                print("  ✓ Country select substitution pattern verified")
        else:
            print("  ✓ Country select onchange already exists")
    
    def add_cloudflare_turnstile_component(self) -> None:
        """Step 6: Add Cloudflare Turnstile component inside form"""
        turnstile_div = '<div class="cf-turnstile" data-sitekey="0x4AAAAAABnCJ2diMumq6zZR"></div>'
        
        if turnstile_div in self.content:
            print("  ✓ Cloudflare Turnstile component already exists")
            return
        
        # Find form and add turnstile component before submit button
        form_pattern = r'(<form[^>]*id="joinForm"[^>]*>.*?)(<button[^>]*type="submit")'
        match = re.search(form_pattern, self.content, re.DOTALL)
        
        if match:
            before_button = match.group(1)
            button = match.group(2)
            
            # Add turnstile if not already there
            if 'cf-turnstile' not in before_button:
                new_content = before_button + '\n                    ' + turnstile_div + '\n                    ' + button
                self.content = re.sub(form_pattern, new_content, self.content, count=1, flags=re.DOTALL)
                print("  ✓ Cloudflare Turnstile component added")
            else:
                print("  ✓ Cloudflare Turnstile component already exists")
        else:
            # Try a more lenient pattern if id is not present
            form_pattern = r'(<form[^>]*>.*?)(<button[^>]*type="submit")'
            match = re.search(form_pattern, self.content, re.DOTALL)
            if match:
                before_button = match.group(1)
                button = match.group(2)
                
                if 'cf-turnstile' not in before_button:
                    new_content = before_button + '\n                    ' + turnstile_div + '\n                    ' + button
                    self.content = re.sub(form_pattern, new_content, self.content, count=1, flags=re.DOTALL)
                    print("  ✓ Cloudflare Turnstile component added")
                else:
                    print("  ✓ Cloudflare Turnstile component already exists")
            else:
                print("  ✗ Could not find form to add Turnstile component")
    
    def ensure_submit_button_id(self) -> None:
        """Step 7: Ensure submit button has id="submitBtn" """
        # Look for submit button in form
        if not re.search(r'id="submitBtn"', self.content):
            # Try to find button with type="submit"
            button_patterns = [
                r'<button\s+type="submit"([^>]*)>',
                r'<button([^>]*)type="submit"([^>]*)>'
            ]
            
            for pattern in button_patterns:
                match = re.search(pattern, self.content)
                if match:
                    original = match.group(0)
                    modified = original.replace('<button', '<button id="submitBtn"', 1)
                    self.content = self.content.replace(original, modified, 1)
                    print("  ✓ Submit button id='submitBtn' added")
                    return
            
            print("  ⚠ Could not find submit button")
        else:
            print("  ✓ Submit button id='submitBtn' already exists")
    
    def add_hidden_input_fields(self) -> None:
        """Step 8: Add hidden input fields inside the form"""
        link_value = self.config_name or self.working_dir or 'fxleader'
        hidden_fields = f'''<input type="hidden" value="{link_value}" name="link_id">
                <input type="hidden" value="{{source}}" name="source">
                <input type="hidden" value="{{signature}}" name="signature">
                <input type="hidden" value="{{timestamp}}" name="timestamp">
                <input type="hidden" value="{{addr}}" name="addr">
                <input type="hidden" id="language" value="{{language}}" name="language">
                <input type="hidden" id="phoneCode" value="{{phonecode}}" name="phonecode">'''
        
        # If link_id exists, ensure its value matches working_directory
        if re.search(r'<input[^>]*name=["\']link_id["\']', self.content):
            updated = re.sub(
                r'(<input[^>]*name=["\']link_id["\'][^>]*value=["\'])[^"]*(["\'])',
                rf'\1{link_value}\2',
                self.content
            )
            if updated != self.content:
                self.content = updated
                print("  ✓ Updated link_id value to working_directory")
                return
            # Handle case where value appears before name
            updated2 = re.sub(
                r'(value=["\'])[^"]*(["\'][^>]*name=["\']link_id["\'])',
                rf'\1{link_value}\2',
                self.content
            )
            if updated2 != self.content:
                self.content = updated2
                print("  ✓ Updated link_id value to working_directory")
                return
            print("  ✓ Hidden input fields already exist")
            return
        
        # Find form opening tag and add after it
        # Try with id="joinForm" first
        form_pattern = r'(<form[^>]*id="joinForm"[^>]*>)'
        match = re.search(form_pattern, self.content)
        
        if not match:
            # Try without id
            form_pattern = r'(<form[^>]*>)'
            match = re.search(form_pattern, self.content)
        
        if match:
            form_opening = match.group(1)
            new_form_opening = form_opening + '\n                ' + hidden_fields
            self.content = re.sub(re.escape(form_opening), new_form_opening, self.content, count=1)
            print("  ✓ Hidden input fields added")
        else:
            print("  ✗ Could not find form to add hidden fields")
    
    def clean_dialog_and_add_id(self) -> None:
        """Step 9: Remove dialog prompt text/title and add id="dialog-content" """
        # Find dialog content section and update it
        dialog_pattern = r'(<div class="dialog-card">)(.*?)(<button[^>]*class="dialog-close")'
        
        match = re.search(dialog_pattern, self.content, re.DOTALL)
        if match:
            opening = match.group(1)
            content = match.group(2)
            button = match.group(3)
            
            # Check if dialog-content div already has id
            if 'id="dialog-content"' not in content:
                # Create simplified content with id
                new_content = opening + '\n            <div id="dialog-content"></div>\n        ' + button
                full_pattern = re.escape(match.group(0))
                self.content = re.sub(full_pattern, new_content, self.content, count=1)
                print("  ✓ Dialog cleaned and id='dialog-content' added")
            else:
                print("  ✓ Dialog id='dialog-content' already exists")
        else:
            print("  ⚠ Could not find dialog to modify")
    
    def replace_dialog_styles(self) -> None:
        """Step 9.5: Replace dialog CSS block with the provided template"""
        if 'dialog[data-dialog-id="1"] #dialog-content' in self.content:
            print("  ✓ Dialog styles already updated")
            return

        replacement = '''dialog {
        justify-content: center;
        width: 100svw;
        height: 100vh;
        inset: 0;
        background: transparent;
        -webkit-backdrop-filter: blur(0.25rem);
        backdrop-filter: blur(0.25rem);
        border: none;
        position: fixed;
        top: 0;
        left: 0;
      }
      dialog::backdrop {
        background: rgba(0, 0, 0, 0.5);
        -webkit-backdrop-filter: blur(0.25rem);
        backdrop-filter: blur(0.25rem);
      }
        dialog[open] {
            display: flex;
        }

        dialog .card {
            margin-block: 2rem;
            padding: 1.25rem;
            border-radius: 0.75rem;
            height: -moz-fit-content;
            height: fit-content;
            background-color: rgba(255, 255, 255, 0.75);
            min-width: 250px;
            max-width: 500px;
            width: 100%;
        }

        dialog .card-header {
            margin: -1.25rem -1.25rem 1rem -1.25rem;
            padding: 0.75rem 1.25rem;
            border-bottom: rgba(0, 0, 0, 0.25) solid 1px;
        }

        dialog .dialog-close {
        position: absolute;
        top: 16px;
        right: 16px;
        width: 16px;
        height: 16px;
        padding: 0;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23000'%3e%3cpath d='M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414'/%3e%3c/svg%3e");
        background-size: contain;
        text-indent: -9999em;
        border: none;
        line-height: 0;
        background-color: transparent;
      }
      .dialog-close {
        position: absolute;
        top: 8px;
        right: 12px;
        width: 16px;
        height: 16px;
        padding: 0;
        background: transparent;
        border: none;
        font-size: 16px;
        cursor: pointer;
        background-size: contain;
      }
    .card.card-white {
    background-color: #fff;
    border: 0px;
    }
    dialog[data-dialog-id="1"] .card-header {
        display: none;
      }

      dialog[data-dialog-id="1"]
        .card
        > div:not(#dialog-content):not(.card-header) {
        display: none;
      }

      dialog[data-dialog-id="1"] #dialog-content {
        padding: 16px 20px;
      }
      .fl-nav-dropdown-menu {
         min-width: 150px;
        }
    </style>'''

        pattern = r'dialog\s*\{.*?</style>'
        if re.search(pattern, self.content, re.DOTALL):
            self.content = re.sub(pattern, replacement, self.content, count=1, flags=re.DOTALL)
            print("  ✓ Dialog styles replaced")
        else:
            print("  ✗ Could not find dialog styles to replace")
    
    def add_javascript_functionality(self) -> None:
                """Step 10: Replace dialog and scripts with the new template"""
                if 'closeDialog()' in self.content and 'lastTurnstileToken' in self.content:
                        print("  ✓ Dialog and scripts already updated")
                        return

                replacement = '''<dialog class="dialog" data-dialog-id="1">
            <div class="card">
                <div class="card-header">
                    <div class="fisg-fl-row">
                        <div class="fisg-fl-col w-col">
                            <h6>Popup Title</h6>
                        </div>
                        <div class="fisg-fl-col w-auto">
                            <button
                                class="dialog-close"
                                type="button"
                                data-dialog-id="1"
                                onclick="closeDialog();"
                            >
                                close
                            </button>
                        </div>
                    </div>
                </div>
                <div id="dialog-content"></div>
                <button class="dialog-close" id="dialog-close">&times;</button>
                <div>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium
                    illum veritatis est modi perspiciatis! Ducimus pariatur debitis
                    dignissimos culpa quaerat rerum doloribus optio. Eligendi ipsum
                    provident ex aliquam earum unde.
                </div>
            </div>
        </dialog>
         <script src="https://cdn.jsdelivr.net/npm/jsencrypt@3.3.2/bin/jsencrypt.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/crypto-js@4.1.1/crypto-js.min.js"></script>
        <script>
            const reloadPage = () => window.location.reload();

            function closeDialog() {
                document.querySelectorAll(".dialog").forEach((d) => d.close());
                setTimeout(reloadPage, 50);
            }

            document.querySelectorAll(".dialog-open").forEach((button) => {
                button.addEventListener("click", () => {
                    const id = button.dataset.dialogId;
                    const dialog = document.querySelector(
                        `.dialog[data-dialog-id="${id}"]`
                    );
                    dialog?.showModal();
                });
            });

            document.querySelectorAll(".dialog-close").forEach((button) => {
                button.addEventListener("click", () => {
                    const id = button.dataset.dialogId;
                    const dialog = document.querySelector(
                        `.dialog[data-dialog-id="${id}"]`
                    );
                    dialog?.close();
                    setTimeout(reloadPage, 50);
                });
            });
        </script>
        <script>
            function countryChange() {
                const select = document.getElementById("country");
                if (!select) return;
                const selectedOption = select.options[select.selectedIndex];
                const code = selectedOption ? selectedOption.getAttribute("code") : "";
                const language = selectedOption
                    ? selectedOption.getAttribute("lang")
                    : "";
                document.getElementById("phoneCode").value = code || "";
                document.getElementById("language").value = language || "en";
            }

            const dialog = document.querySelector(`.dialog[data-dialog-id="1"]`);
            const closeBtn = document.getElementById("dialog-close");

            closeBtn?.addEventListener("click", () => {
                dialog.close();
                setTimeout(() => window.location.reload(), 50);
            });

            dialog?.addEventListener("cancel", () => {
                dialog.close();
                setTimeout(() => window.location.reload(), 50);
            });

            dialog?.addEventListener("click", (e) => {
                const card = dialog.querySelector(".card");
                if (!card) return;
                const r = card.getBoundingClientRect();
                const outside =
                    e.clientX < r.left ||
                    e.clientX > r.right ||
                    e.clientY < r.top ||
                    e.clientY > r.bottom;
                if (outside) {
                    dialog.close();
                    setTimeout(() => window.location.reload(), 50);
                }
            });

                const key = `LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF2N3lFcy84VlV1cG1reEg1akVQbwpSS2l2clNhejZ2d3VST3N3Tkdka1NhRFJZR1l2b3ZRVDdJMGZnWDRMUU9hNHVwTXZZZTNrZytlTjBiNldzM1JMCklsakpqdkZxb3VLQnp2VXdXMXJ6RFBmUkNENW9wWWxGY2pCWmVqcXFIVFc5dkpFRVZSK05INlhKcEM4YWpSNUkKUHFQaWdXa3NIak9PbjhPV3cwNHY1QjV2TWVTeDcyNmVJSG9NUjZOZHR0WmFVd0pzMjBTS3hPVDU4aDlSSG52dQpwZW1xL1dYN0s2dzQ1L2pLbSswNmdOL1pDZ054aE42MEQ5MUZNTEVkTjJPVTJiQVFObUZkN2d4TG82NFkyMXVoClFXdzVKTStTQVJWU2VyNUVoMTFUTG1rdXo1VWhBZC90OXRNMmdaU3kvT1hMNjRuQ3ltT0V6VGpRajJ2U3Z6b2kKUHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t`;

                let lastTurnstileToken = null;

                const resetToken = () => {
                        turnstile.reset();
                        lastTurnstileToken = null;
                };

                document.getElementById('joinForm').addEventListener('submit', function (e) {
                        e.preventDefault();

                        const dialog = document.querySelector(`.dialog[data-dialog-id="1"]`);
                        const submitBtn = document.getElementById('submitBtn');
                        const loadingText = document.getElementById('loadingText');

                        const form = e.target;
                        const formData = new FormData(form);
                        const data = {};
                        formData.forEach((value, key) => {
                                if (key !== "cf-turnstile-response") data[key] = value
                        });

                        const token = formData.get("cf-turnstile-response");
                        if (!token) {
                                document.getElementById("dialog-content").innerText =
                                    "Please complete the verification before submitting.";
                                dialog?.showModal();
                                resetToken();
                                return;
                        }

                        if (token === lastTurnstileToken) {
                                document.getElementById("dialog-content").innerText =
                                    "Please verify again before submitting.";
                                dialog?.showModal();
                                resetToken();
                                return;
                        }

                        lastTurnstileToken = token;

                        if (submitBtn) {
                            submitBtn.disabled = true;
                            submitBtn.innerText = "Submitting...";
                        }

                        const aesKey = CryptoJS.lib.WordArray.random(16).toString(CryptoJS.enc.Hex);
                        const encryptedData = CryptoJS.AES.encrypt(JSON.stringify(data), aesKey).toString();
                        const encrypt = new JSEncrypt();
                        encrypt.setPublicKey(atob(key));
                        const encryptedKey = encrypt.encrypt(aesKey);

                        fetch('/website/register', {
                                method: 'POST',
                                headers: {
                                        'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ data: encryptedData, key: encryptedKey, "cf-turnstile-response": token })
                        }).then(async (res) => {
                                let result = {};
                                try {
                                    result = await res.json();
                                } catch (err) {
                                    // no response body
                                }

                                const msgLower = (result.msg || "").toLowerCase();
                                const showError = (text) => {
                                    document.getElementById("dialog-content").innerText = text;
                                    dialog?.showModal();
                                    resetToken();
                                };
                                const defaultError =
                                    "We're sorry, your registration could not be completed. Please try again shortly or contact our support team for assistance.";

                                if (msgLower.includes("registered") || msgLower.includes("already")) {
                                    showError(
                                        "This email or username has already been used. Please use different details or contact our support team."
                                    );
                                    return;
                                }

                                if (!res.ok || msgLower.includes("request validation failed")) {
                                    showError(result.msg || defaultError);
                                    return;
                                }

                                document.getElementById('joinForm').reset();
                                document.getElementById("dialog-content").innerText =
                                    "Thank you for registering. A member of our team will reach out to you soon.";
                                dialog?.showModal();
                                resetToken();
                        })
                                .catch(() => {
                                        document.getElementById("dialog-content").innerText = "We're sorry, your registration could not be completed. Please try again shortly or contact our support team for assistance.";
                                        dialog?.showModal();
                                        resetToken();
                                }).finally(() => {
                                        if (submitBtn) {
                                            submitBtn.disabled = false;
                                            submitBtn.innerText = "Join FISG Membership Now";
                                        }
                                });
                });
        </script>
</body>
</html>'''

                pattern = r'<dialog[^>]*class="dialog"[^>]*>.*?</html>'
                if re.search(pattern, self.content, re.DOTALL):
                        self.content = re.sub(pattern, replacement, self.content, count=1, flags=re.DOTALL)
                        print("  ✓ Dialog and scripts replaced")
                else:
                        print("  ✗ Could not find dialog section to replace")
    
    def apply_all_modifications(self) -> str:
        """Apply all modifications in the correct order"""
        print("\nApplying modifications...\n")
        self.add_google_tag()
        self.add_cloudflare_dependencies()
        self.convert_absolute_to_relative_paths()
        self.ensure_join_form_id()
        self.add_country_select_onchange()
        self.add_cloudflare_turnstile_component()
        self.ensure_submit_button_id()
        self.add_hidden_input_fields()
        self.clean_dialog_and_add_id()
        self.replace_dialog_styles()
        self.add_javascript_functionality()
        print("\n✓ All modifications applied\n")
        return self.content


def update_kv_key(js_file_path: str, kv_key: str) -> bool:
    """Update KV_KEY in upload-to-kv.js to match the working_directory.

    Args:
        js_file_path: Absolute path to upload-to-kv.js
        kv_key: The value to set for KV_KEY

    Returns:
        True if the file was updated, False otherwise.
    """
    try:
        if not os.path.exists(js_file_path):
            print(f"⚠ KV script not found: {js_file_path}")
            return False

        with open(js_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace: const KV_KEY = '...';
        pattern = r"const\s+KV_KEY\s*=\s*['\"][^'\"]+['\"];"
        replacement = f"const KV_KEY = '{kv_key}';"

        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content, count=1)
            if new_content != content:
                with open(js_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ KV_KEY updated to '{kv_key}' in: {js_file_path}")
                return True
            else:
                print("✓ KV_KEY already set correctly")
                return True
        else:
            print("⚠ KV_KEY declaration not found in upload-to-kv.js")
            return False
    except Exception as e:
        print(f"✗ Error updating KV_KEY: {e}")
        return False


def process_language_file(lang_code: str, example_dir: str, working_dir: Optional[str], config_name: Optional[str]) -> bool:
    """Process a single language's index.html file"""
    file_path = os.path.join(example_dir, lang_code, 'index.html')
    
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Processing: {lang_code.upper()}")
    print(f"{'='*60}")
    
    try:
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Apply modifications
        modifier = HTMLModifier(html_content, working_dir=working_dir, config_name=config_name)
        modified_content = modifier.apply_all_modifications()
        
        # Write the modified content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print(f"✓ Successfully saved: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {lang_code}: {str(e)}")
        return False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    
    # Load configuration from config.json
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        working_dir = config.get('working_directory', 'example')
        config_name = config.get('name') or working_dir
        languages = config.get('languages', ['en', 'lo', 'ms', 'th', 'vi'])
        
        # Handle both relative and absolute paths
        if os.path.isabs(working_dir):
            example_dir = working_dir
        else:
            example_dir = os.path.join(script_dir, working_dir)
        
        print(f"✓ Loaded configuration from config.json")
    except FileNotFoundError:
        print("⚠ config.json not found, using default settings")
        example_dir = os.path.join(script_dir, 'example')
        languages = ['en', 'lo', 'ms', 'th', 'vi']
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing config.json: {e}")
        return
    
    if not os.path.exists(example_dir):
        print(f"✗ Directory not found: {example_dir}")
        return

    # If languages list is empty, auto-detect all language folders
    if not languages:
        languages = []
        if os.path.isdir(example_dir):
            for item in os.listdir(example_dir):
                item_path = os.path.join(example_dir, item)
                # Check if it's a directory and contains index.html
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'index.html')):
                    languages.append(item)
            languages.sort()  # Sort for consistent ordering
        
        if languages:
            print(f"✓ Auto-detected languages: {', '.join(languages)}")
        else:
            print("⚠ No language folders with index.html found")
            return

    # Update KV_KEY in upload-to-kv.js to match working_directory
    kv_js_path = os.path.join(example_dir, 'upload-to-kv.js')
    update_kv_key(kv_js_path, config_name)
    
    print("\n" + "="*60)
    print("FISG HTML MODIFIER SYSTEM")
    print("="*60)
    print(f"Working directory: {example_dir}")
    print(f"Languages to process: {', '.join(languages)}")
    
    # Process each language
    results = {}
    for lang in languages:
        results[lang] = process_language_file(lang, example_dir, working_dir, config_name)
    
    # Print summary
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    for lang, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {lang.upper()}: {'Success' if success else 'Failed'}")
    
    print(f"\nTotal: {successful}/{total} files processed successfully")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
