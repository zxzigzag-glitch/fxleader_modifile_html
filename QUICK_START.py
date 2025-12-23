#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Usage Guide for FISG HTML Modifier System
ระบบแก้ไข HTML สำหรับ FISG Landing Pages
"""

print("""
================================================================================
                   FISG HTML MODIFIER SYSTEM - QUICK START
================================================================================

📋 ฟังก์ชันหลัก (Main Function):
   ปรับปรุง index.html ใน 5 ภาษา (EN, LO, MS, TH, VI) ตามคำสั่ง fxleader.md

📁 ไฟล์ที่เกี่ยวข้อง:
   • modify_html.py         - Python script หลัก
   • SYSTEM_README.md       - ข้อมูลระบบโดยละเอียด
   • fxleader.md            - คำสั่งการแก้ไข (10 ขั้นตอน)
   • example/en/index.html  - ไฟล์ที่แก้ไข (ทั้ง 5 ภาษา)
   • example/lo/index.html
   • example/ms/index.html
   • example/th/index.html
   • example/vi/index.html

🚀 วิธีใช้ (How to Run):
   
   cd /Users/lp-03/fxleader_modifile_html
   python3 modify_html.py

✅ 10 ขั้นตอนที่แก้ไข (10 Modifications):
   
   1.  ✓ Google Tag Manager (G-XEYRPJNWLJ)
   2.  ✓ Cloudflare Turnstile Dependencies (Bootstrap + Icons + API)
   3.  ✓ URL Conversion (https://www.fisg.com/ → /)
   4.  ✓ Form ID (id="joinForm")
   5.  ✓ Country Select Event (onchange="countryChange()")
   6.  ✓ Cloudflare Turnstile Component (CAPTCHA div)
   7.  ✓ Submit Button ID (id="submitBtn")
   8.  ✓ Hidden Input Fields (link_id, source, signature, timestamp, addr, 
                              language, phonecode)
   9.  ✓ Dialog Cleanup (id="dialog-content")
   10. ✓ JavaScript Functionality (encryption, form submission)

📊 ผลลัพธ์ (Results):
   
   ทั้ง 5 ไฟล์ index.html ได้รับการแก้ไขตามคำสั่งอย่างสมบูรณ์
   • EN version ✓
   • LO version ✓
   • MS version ✓
   • TH version ✓
   • VI version ✓

🔄 การรัน Script ซ้ำ (Idempotent):
   
   สามารถรัน script ได้หลายครั้งโดยไม่ทำให้ duplicate changes
   เนื่องจาก script มีการตรวจสอบก่อนการแก้ไข

💡 ตัวอย่างการเปลี่ยนแปลง (Example):

   Before: <link rel="icon" href="https://www.fisg.com/wp-content/..." />
   After:  <link rel="icon" href="/wp-content/..." />

   Before: <form action="">
   After:  <form id="joinForm" action="">
           <input type="hidden" value="fxleader" name="link_id">
           ...

   Before: <button type="submit">Start Your Trading Journey</button>
   After:  <button type="submit" id="submitBtn">Start Your Trading...</button>
           <div class="cf-turnstile" data-sitekey="..."></div>

🛠️ เทคนิค (Technical):
   • Language: Python 3
   • Approach: Regular Expression Matching & Replacement
   • Design: Idempotent (safe to run multiple times)
   • Support: 5 languages (EN, LO, MS, TH, VI)

📌 Notes:
   • ไฟล์ถูกเก็บไว้ใน git repository
   • สามารถ reset ได้โดย: git checkout example/*/index.html
   • script ทำงานโดยอัตโนมัติสำหรับทั้ง 5 ไฟล์

🎯 ทำไมต้องแก้ไข:
   ✓ Google Analytics tracking
   ✓ Bot protection (Cloudflare Turnstile)
   ✓ Consistent URLs (relative paths)
   ✓ Proper form structure
   ✓ Data encryption & security
   ✓ User experience improvements

📞 Support:
   For detailed info: cat SYSTEM_README.md
   For requirements: cat fxleader.md

================================================================================
""")
