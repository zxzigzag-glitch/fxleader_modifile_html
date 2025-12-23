Wayne provided the original source files, and I am sending the modified example files.

Other landing pages in the production environment
https://www.fisg.com/en/landing/myfxbook-membership

1. Add the corresponding Google Tag in the head section (example file lines 5-12).
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XEYRPJNWLJ"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-XEYRPJNWLJ');
</script>

2. Add Cloudflare Turnstile dependency files (example file lines 13-20).
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.1/css/bootstrap.min.css"
        integrity="sha512-siwe/oXMhSjGCwLn+scraPOWrJxHlUgMBMZXdPe2Tnk3I0x3ESCoLz7WZ5NTH6SZrywMY+PB1cjyqJ5jAluCOg=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
<link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.9.1/font/bootstrap-icons.min.css"
        integrity="sha512-5PV92qsds/16vyYIJo3T/As4m2d8b6oWYfoqV+vtizRB6KhF1F9kYzWzQmsO6T3z3QG2Xdhrx7FQ+5R1LiQdUA=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" defer></script>

3. Change all href references starting with https://www.fisg.com/ to root-relative paths.
Example:
<link rel="icon" href="https://www.fisg.com/wp-content/uploads/2025/01/cropped-logo-icon-32x32.png" sizes="32x32" />
should be changed to
<link rel="icon" href="/wp-content/uploads/2025/01/cropped-logo-icon-32x32.png" sizes="32x32" />

Regarding the form, please refer to the example file and check if the form validation matches the example.

4. Check if the page contains a form with id="joinForm". If it does not exist, add it.
Example:
<form class="fisg-ms-join-form card card-white" id="joinForm" action="">

5. In the form, for the country select element, add an onchange event and variable substitution.
Example:
<select name="country" id="country" required onchange="countryChange()">
{{select:country}}

6. Add the Cloudflare Turnstile component inside the form submit button area (this must be inside the form).
Example:
<div class="cf-turnstile" data-sitekey="0x4AAAAAABnCJ2diMumq6zZR"></div>

7. Check the form submit button for existence of id="submitBtn". If it doesn't exist, add it.
Example:
<button type="submit" id="submitBtn">Join FISG Membership Now</button>

8. Add the following hidden input fields inside the form:
<input type="hidden" value="fxleader" name="link_id">
<input type="hidden" value="{{source}}" name="source">
<input type="hidden" value="{{signature}}" name="signature">
<input type="hidden" value="{{timestamp}}" name="timestamp">
<input type="hidden" value="{{addr}}" name="addr">
<input type="hidden" id="language" value="{{language}}" name="language">
<input type="hidden" id="phoneCode" value="{{phonecode}}" name="phonecode">

9. Remove the prompt text and title from the dialog, and add id="dialog-content" to the content container (example file lines 2054-2066).

10. Copy the following script block directly; you may adjust the prompt messages as needed.
<script src="https://cdn.jsdelivr.net/npm/jsencrypt@3.3.2/bin/jsencrypt.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/crypto-js@4.1.1/crypto-js.min.js"></script>
<script>
    function countryChange() {
        const select = document.getElementById('country');
        const selectedOption = select.options[select.selectedIndex];
        const code = selectedOption.getAttribute('code');
        const language = selectedOption.getAttribute('lang');

        document.getElementById('phoneCode').value = code || '';
        document.getElementById('language').value = language || 'en';
    }
    document.querySelectorAll(".dialog-open").forEach(button => {
            button.addEventListener("click", () => {
                const id = button.dataset.dialogId;
                const dialog = document.querySelector(`.dialog[data-dialog-id="${id}"]`);
                dialog?.show();
            });
        });

        document.querySelectorAll(".dialog-close").forEach(button => {
            button.addEventListener("click", () => {
                const id = button.dataset.dialogId;
                const dialog = document.querySelector(`.dialog[data-dialog-id="${id}"]`);
                dialog?.close();
            });
        });

        const key = `LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF2N3lFcy84VlV1cG1reEg1akVQbwpSS2l2clNhejZ2d3VST3N3Tkdka1NhRFJZR1l2b3ZRVDdJMGZnWDRMUU9hNHVwTXZZZTNrZytlTjBiNldzM1JMCklsakpqdkZxb3VLQnp2VXdXMXJ6RFBmUkNENW9wWWxGY2pCWmVqcXFIVFc5dkpFRVZSK05INlhKcEM4YWpSNUkKUHFQaWdXa3NIak9PbjhPV3cwNHY1QjV2TWVTeDcyNmVJSG9NUjZOZHR0WmFVd0pzMjBTS3hPVDU4aDlSSG52dQpwZW1xL1dYN0s2dzQ1L2pLbSswNmdOL1pDZ054aE42MEQ5MUZNTEVkTjJPVTJiQVFObUZkN2d4TG82NFkyMXVoClFXdzVKTStTQVJWU2VyNUVoMTFUTG1rdXo1VWhBZC90OXRNMmdaU3kvT1hMNjRuQ3ltT0V6VGpRajJ2U3Z6b2kKUHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t`;

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
            // console.log("data", data);

            submitBtn.disabled = true;
            submitBtn.innerText = "Submitting...";


            const aesKey = CryptoJS.lib.WordArray.random(16).toString(CryptoJS.enc.Hex); // 128
            const encryptedData = CryptoJS.AES.encrypt(JSON.stringify(data), aesKey).toString();
            // RSA to AES
            const encrypt = new JSEncrypt();
            encrypt.setPublicKey(atob(key));
            const encryptedKey = encrypt.encrypt(aesKey);

            // request fetch POST
            fetch('/website/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data: encryptedData, key: encryptedKey, "cf-turnstile-response": formData.get("cf-turnstile-response") })
            }).then(res => res.json())
                .then(result => {
                    let { msg } = result
                    if (msg == "ok") {
                        document.getElementById('joinForm').reset();
                        msg = "Thank you for registering. A member of our team will reach out to you soon."
                    }
                    document.getElementById("dialog-content").innerText = msg
                    dialog?.show();
                })
                .catch(err => {
                    console.error('reqeust filed: ', err);
                    document.getElementById("dialog-content").innerText = "We're sorry, your registration could not be completed. Please try again shortly or contact our support team for assistance."
                    dialog?.show();
                }).finally(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerText = "Join FISG Membership Now";
                });
        });
</script>