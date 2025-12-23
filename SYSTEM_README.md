# FISG HTML Modifier System

ระบบแก้ไข HTML สำหรับหน้าแนวทางการลงทะเบียน FISG ด้วย Python

## สรุป (Overview)

`modify_html.py` เป็นระบบ Python ที่ใช้ในการแก้ไขไฟล์ `index.html` ในหลายภาษา (EN, LO, MS, TH, VI) ตามคำสั่งในไฟล์ `fxleader.md`

## ความสามารถ (Features)

ระบบจะทำการแก้ไข 11 ขั้นตอนตามที่กำหนด:

1. **เพิ่ม Google Tag Manager** - เพิ่ม Google Analytics tracking code (G-XEYRPJNWLJ)
2. **เพิ่ม Cloudflare Turnstile Dependencies** - เพิ่ม Bootstrap และ Turnstile CSS/JS
3. **แปลง Absolute Paths เป็น Relative Paths** - เปลี่ยน `https://www.fisg.com/...` เป็น `/...` (รวมถึง fix double-slash)
4. **เพิ่ม Form ID** - เพิ่ม `id="joinForm"` ให้กับแบบฟอร์ม
5. **เพิ่ม Country Select Event** - เพิ่ม `onchange="countryChange()"` ให้กับ select element
6. **เพิ่ม Cloudflare Turnstile Component** - เพิ่ม CAPTCHA div
7. **เพิ่ม Submit Button ID** - เพิ่ม `id="submitBtn"` ให้กับปุ่ม submit
8. **เพิ่ม Hidden Input Fields** - เพิ่มฟิลด์ที่ซ่อน (link_id ใช้ค่าจาก config name, source, signature, timestamp, addr, language, phonecode)
9. **ทำความสะอาด Dialog** - ลบ prompt text และเพิ่ม `id="dialog-content"`
10. **แทนที่ Dialog Styles** - แทนที่ CSS ของ dialog ด้วย template ใหม่
11. **แทนที่ JavaScript และ Dialog HTML** - แทนที่ทั้ง dialog block และ scripts ด้วย template ใหม่ (รวม encryption, form submission)

## การใช้งาน (Usage)

### ข้อกำหนดเบื้องต้น (Requirements)
- Python 3.6+

### การตั้งค่า (Configuration)

แก้ไขไฟล์ `config.json`:

```json
{
  "name": "example222",
  "working_directory": "example",
  "languages": ["en", "lo", "ms", "th", "vi"]
}
```

- **name**: ชื่อที่ใช้สำหรับ link_id และ KV_KEY
- **working_directory**: โฟลเดอร์ที่มีไฟล์ HTML (รองรับ relative และ absolute paths)
- **languages**: รายการภาษาที่ต้องการประมวลผล (ถ้าว่าง `[]` จะ auto-detect ทุกโฟลเดอร์ที่มี index.html)

### การรัน (Running)

```bash
cd /Users/lp-03/fxleader_modifile_html
python3 modify_html.py
```

### Output Example

```
✓ Loaded configuration from config.json
✓ Auto-detected languages: en, lo, ms, th, vi
✓ KV_KEY updated to 'example222' in: /Users/lp-03/fxleader_modifile_html/example/upload-to-kv.js

============================================================
FISG HTML MODIFIER SYSTEM
============================================================
Working directory: /Users/lp-03/fxleader_modifile_html/example
Languages to process: en, lo, ms, th, vi

============================================================
Processing: EN
============================================================

Applying modifications...

  ✓ Google Tag added
  ✓ Cloudflare dependencies added
  ✓ Converted 11 absolute paths to relative paths
  ✓ Form id='joinForm' added/verified
  ✓ Country select substitution pattern verified
  ✓ Cloudflare Turnstile component added
  ✓ Submit button id='submitBtn' added
  ✓ Hidden input fields added
  ✓ Dialog cleaned and id='dialog-content' added
  ✓ Dialog styles replaced
  ✓ JavaScript functionality and dialog HTML replaced

✓ All modifications applied

✓ Successfully saved: /Users/lp-03/fxleader_modifile_html/example/en/index.html
...

============================================================
PROCESSING SUMMARY
============================================================
✓ EN: Success
✓ LO: Success
✓ MS: Success
✓ TH: Success
✓ VI: Success

Total: 5/5 files processed successfully
============================================================
```

## โครงสร้างไฟล์ (File Structure)

```
/Users/lp-03/fxleader_modifile_html/
├── modify_html.py              # Python script หลัก (~760 lines)
├── config.json                 # Configuration file (working_directory, languages, name)
├── fxleader.md                 # คำสั่งการแก้ไข
├── README.md
├── SYSTEM_README.md            # ไฟล์นี้
├── INDEX.md
└── example/
    ├── upload-to-kv.js        # KV upload script (KV_KEY จะถูก auto-update)
    ├── en/index.html          # English version (แก้ไขแล้ว)
    ├── lo/index.html          # Lao version (แก้ไขแล้ว)
    ├── ms/index.html          # Malay version (แก้ไขแล้ว)
    ├── th/index.html          # Thai version (แก้ไขแล้ว)
    └── vi/index.html          # Vietnamese version (แก้ไขแล้ว)
```

## Classes และ Methods

### HTMLModifier Class

ระบบใช้คลาส `HTMLModifier(html_content, working_dir=None, config_name=None)` ที่มี methods ต่อไปนี้:

- `__init__(html_content, working_dir, config_name)` - สร้าง instance พร้อม content และ config values
- `add_google_tag()` - เพิ่ม Google Tag Manager (G-XEYRPJNWLJ)
- `add_cloudflare_dependencies()` - เพิ่ม Cloudflare dependencies (Bootstrap, Icons, Turnstile API)
- `convert_absolute_to_relative_paths()` - แปลง URLs และ fix double-slash
- `ensure_join_form_id()` - เพิ่ม form ID (id="joinForm")
- `add_country_select_onchange()` - เพิ่ม event handler (onchange="countryChange()")
- `add_cloudflare_turnstile_component()` - เพิ่ม CAPTCHA div
- `ensure_submit_button_id()` - เพิ่ม button ID (id="submitBtn")
- `add_hidden_input_fields()` - เพิ่ม hidden fields (ใช้ config_name สำหรับ link_id value)
- `clean_dialog_and_add_id()` - ทำความสะอาด dialog และเพิ่ม id="dialog-content"
- `replace_dialog_styles()` - แทนที่ dialog CSS ทั้งหมด
- `add_javascript_functionality()` - แทนที่ dialog HTML และ JavaScript ทั้งหมด
- `apply_all_modifications()` - รัน all 11 steps ตามลำดับ

### Supporting Functions

- `update_kv_key(js_file_path, kv_key)` - อัพเดท KV_KEY ใน upload-to-kv.js
- `process_language_file(lang_code, example_dir, working_dir, config_name)` - ประมวลผลไฟล์ HTML แต่ละภาษา
- `main()` - โหลด config.json, auto-detect languages (ถ้า languages ว่าง), update KV_KEY, และประมวลผลทุกภาษา

## Technical Details

- **Language**: Python 3.6+ (stdlib only - ไม่ต้องติดตั้ง external packages)
- **Regex-based**: ใช้ regular expressions สำหรับการค้นหาและแทนที่
- **Idempotent**: สามารถรัน multiple times โดยไม่ทำให้ duplicate
- **Config-driven**: ใช้ config.json ในการกำหนด working directory, languages, และ dynamic values
- **Auto-detect**: ถ้า languages ใน config ว่าง จะ auto-detect โฟลเดอร์ที่มี index.html อัตโนมัติ
- **Multi-language Support**: รองรับหลายภาษาตามที่กำหนดใน config หรือ auto-detect
- **KV_KEY Sync**: อัพเดท KV_KEY ใน upload-to-kv.js ให้ตรงกับ config name อัตโนมัติ
- **Dynamic Values**: ใช้ config['name'] สำหรับ link_id และ KV_KEY (fallback เป็น working_directory)

## ตัวอย่างการเปลี่ยนแปลง (Example Changes)

### Before
```html
<form action="">
    <div class="fl-form-column">
        <input type="text" id="name" required>
        <select name="" id="country">
        ...
        <button type="submit">Start Your Trading Journey</button>
```

### After
```html
<form id="joinForm" action="">
    <input type="hidden" value="example222" name="link_id">  <!-- ค่าจาก config.json name -->
    <input type="hidden" value="{{source}}" name="source">
    <input type="hidden" value="{{signature}}" name="signature">
    <input type="hidden" value="{{timestamp}}" name="timestamp">
    <input type="hidden" value="{{addr}}" name="addr">
    <input type="hidden" id="language" value="{{language}}" name="language">
    <input type="hidden" id="phoneCode" value="{{phonecode}}" name="phonecode">
    <div class="fl-form-column">
        <input type="text" id="name" required>
        <select name="" id="country" required onchange="countryChange()">
        ...
        <div class="cf-turnstile" data-sitekey="0x4AAAAAABnCJ2diMumq6zZR"></div>
        <button type="submit" id="submitBtn">Start Your Trading Journey</button>
```

### upload-to-kv.js
```javascript
// ก่อน
const KV_KEY = 'example';

// หลัง (อัพเดทอัตโนมัติจาก config.json name)
const KV_KEY = 'example222';
```

## JavaScript Features

ฟีเจอร์ JavaScript ที่เพิ่มเข้ามา:

- `countryChange()` - ฟังก์ชันสำหรับจัดการการเลือกประเทศและอัพเดท phonecode, language
- `closeDialog()` - ปิด dialog และ reload หน้า
- Dialog Event Listeners - เปิด/ปิด dialog ด้วยปุ่มและคลิกนอก dialog
- Turnstile Token Management - เก็บและตรวจสอบ token เพื่อป้องกันการ submit ซ้ำ
- RSA + AES Encryption - เข้ารหัสข้อมูลฟอร์มด้วย JSEncrypt และ CryptoJS
- Form Submission - POST ไปยัง `/website/register` พร้อม encrypted data
- Error Handling - แสดง error messages ใน dialog พร้อม reset token
- Loading State - แสดงสถานะ "Submitting..." ขณะส่งข้อมูล

## Configuration Examples

### ใช้งานกับโฟลเดอร์อื่น
```json
{
  "name": "fastbull-landing",
  "working_directory": "../fastbull-landing",
  "languages": ["en", "th"]
}
```

### Auto-detect ทุกภาษา
```json
{
  "name": "my-project",
  "working_directory": "example",
  "languages": []  // ว่าง = auto-detect ทุกโฟลเดอร์ที่มี index.html
}
```

### ใช้ absolute path
```json
{
  "name": "production",
  "working_directory": "/Users/username/projects/my-landing",
  "languages": ["en"]
}
```

## Notes

- **Idempotent design** - สามารถรัน script หลายครั้งได้โดยไม่ทำให้ duplicate
- **Config-driven** - เปลี่ยน working directory ได้ง่ายผ่าน config.json
- **Auto-detect** - ถ้า languages ว่าง จะ scan และประมวลผลทุกโฟลเดอร์ที่มี index.html
- **KV_KEY sync** - อัพเดท upload-to-kv.js อัตโนมัติให้ตรงกับ config name
- **Dynamic values** - link_id และ KV_KEY ใช้ค่าจาก config['name']
- **Support multiple HTML structures** - regex patterns ยืดหยุ่นรองรับ HTML หลายรูปแบบ
- **Comprehensive error reporting** - แสดงผลลัพธ์แต่ละขั้นตอนและสรุปท้ายสุด

## Support

สำหรับความเห็นหรือปัญหา:
- ดูไฟล์ `fxleader.md` สำหรับข้อกำหนดเดิม
- ดูไฟล์ `config.json` สำหรับการตั้งค่า
- ตรวจสอบ terminal output สำหรับรายละเอียด error
