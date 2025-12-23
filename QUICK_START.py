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
   ปรับปรุง index.html ในหลายภาษาตามคำสั่ง fxleader.md
   ใช้ config.json ในการกำหนดค่า (working_directory, languages, name)

📁 ไฟล์ที่เกี่ยวข้อง:
   • modify_html.py             - Python script หลัก (~760 lines)
   • config.json                - Configuration file (NEW)
   • SYSTEM_README.md           - ข้อมูลระบบโดยละเอียด
   • fxleader.md                - คำสั่งการแก้ไข
   • {working_directory}/*/index.html - ไฟล์ที่แก้ไข (auto-detect หรือระบุใน config)
   • {working_directory}/upload-to-kv.js - KV upload script (auto-update KV_KEY)

🚀 วิธีใช้ (How to Run):
   
   1. แก้ไข config.json:
      {
        "name": "example222",
        "working_directory": "example",
        "languages": ["en", "th"]  // หรือ [] เพื่อ auto-detect
      }
   
   2. รัน script:
      cd /Users/lp-03/fxleader_modifile_html
      python3 modify_html.py

✅ 11 ขั้นตอนที่แก้ไข (11 Modifications):
   
   1.  ✓ Google Tag Manager (G-XEYRPJNWLJ) - วางหลัง <head>
   2.  ✓ Cloudflare Turnstile Dependencies (Bootstrap + Icons + API) - วางก่อน <style>
   3.  ✓ URL Conversion (https://www.fisg.com/ → /) + fix double-slash
   4.  ✓ Form ID (id="joinForm")
   5.  ✓ Country Select Event (onchange="countryChange()")
   6.  ✓ Cloudflare Turnstile Component (CAPTCHA div)
   7.  ✓ Submit Button ID (id="submitBtn")
   8.  ✓ Hidden Input Fields (link_id ใช้ค่าจาก config name, source, signature, 
                              timestamp, addr, language, phonecode)
   9.  ✓ Dialog Cleanup (id="dialog-content")
   10. ✓ Dialog Styles Replacement (แทนที่ CSS ทั้งหมด)
   11. ✓ JavaScript & Dialog HTML (แทนที่ dialog + scripts ทั้งหมด)

📊 ผลลัพธ์ (Results):
   
   ไฟล์ index.html ทั้งหมดได้รับการแก้ไขตามคำสั่งอย่างสมบูรณ์
   • ประมวลผลภาษาตามที่ระบุใน config.json
   • หรือ auto-detect ทุกโฟลเดอร์ที่มี index.html (ถ้า languages = [])
   • KV_KEY ใน upload-to-kv.js อัพเดทอัตโนมัติ
   • link_id ใช้ค่าจาก config name
   • ทุกขั้นตอน 11 steps ✓

🔄 การรัน Script ซ้ำ (Idempotent):
   
   สามารถรัน script ได้หลายครั้งโดยไม่ทำให้ duplicate changes
   เนื่องจาก script มีการตรวจสอบก่อนการแก้ไข

💡 ตัวอย่างการเปลี่ยนแปลง (Example):

   Before: <link rel="icon" href="https://www.fisg.com/wp-content/..." />
   After:  <link rel="icon" href="/wp-content/..." />

   Before: <form action="">
   After:  <form id="joinForm" action="">
           <input type="hidden" value="example222" name="link_id">  <!-- จาก config.json name -->
           ...

   Before: <button type="submit">Start Your Trading Journey</button>
   After:  <button type="submit" id="submitBtn">Start Your Trading...</button>
           <div class="cf-turnstile" data-sitekey="..."></div>

   upload-to-kv.js:
   Before: const KV_KEY = 'example';
   After:  const KV_KEY = 'example222';  // auto-update จาก config.json name

🛠️ เทคนิค (Technical):
   • Language: Python 3.6+ (stdlib only)
   • Configuration: JSON-based config file
   • Approach: Regular Expression Matching & Replacement
   • Design: Idempotent + Config-driven (safe to run multiple times)
   • Support: หลายภาษา (auto-detect หรือระบุใน config)
   • Paths: รองรับทั้ง relative และ absolute paths
   • Dynamic Values: link_id และ KV_KEY ใช้ค่าจาก config.json

📌 Notes:
   • ไฟล์ถูกเก็บไว้ใน git repository
   • สามารถ reset ได้โดย: git checkout {working_directory}/*/index.html
   • script ทำงานโดยอัตโนมัติสำหรับทุกภาษาที่กำหนด
   • ใช้ config.json ในการควบคุมการทำงาน
   • auto-detect languages ถ้า languages = [] ใน config
   • KV_KEY อัพเดทอัตโนมัติให้ตรงกับ config name
   • รองรับการใช้งานกับหลาย projects (เปลี่ยน working_directory ได้)

🎯 ทำไมต้องแก้ไข:
   ✓ Google Analytics tracking (G-XEYRPJNWLJ)
   ✓ Bot protection (Cloudflare Turnstile CAPTCHA)
   ✓ Consistent URLs (relative paths + fix double-slash)
   ✓ Proper form structure
   ✓ Data encryption & security (RSA + AES)
   ✓ Dynamic values (config-driven link_id, KV_KEY)
   ✓ Enhanced dialog & error handling
   ✓ User experience improvements
   ✓ Multi-project support (config.json)

📞 Support:
   For detailed info: cat SYSTEM_README.md
   For configuration: cat config.json
   For requirements: cat fxleader.md
   For doc index: cat INDEX.md

================================================================================
""")
