# FISG HTML Modifier System

ระบบแก้ไข HTML สำหรับหน้าแนวทางการลงทะเบียน FISG ด้วย Python

## สรุป (Overview)

`modify_html.py` เป็นระบบ Python ที่ใช้ในการแก้ไขไฟล์ `index.html` ในหลายภาษา (EN, LO, MS, TH, VI) ตามคำสั่งในไฟล์ `fxleader.md`

## ความสามารถ (Features)

ระบบจะทำการแก้ไข 10 ขั้นตอนตามที่กำหนด:

1. **เพิ่ม Google Tag Manager** - เพิ่ม Google Analytics tracking code
2. **เพิ่ม Cloudflare Turnstile Dependencies** - เพิ่ม Bootstrap และ Turnstile CSS/JS
3. **แปลง Absolute Paths เป็น Relative Paths** - เปลี่ยน `https://www.fisg.com/...` เป็น `/...`
4. **เพิ่ม Form ID** - เพิ่ม `id="joinForm"` ให้กับแบบฟอร์ม
5. **เพิ่ม Country Select Event** - เพิ่ม `onchange="countryChange()"` ให้กับ select element
6. **เพิ่ม Cloudflare Turnstile Component** - เพิ่ม CAPTCHA div
7. **เพิ่ม Submit Button ID** - เพิ่ม `id="submitBtn"` ให้กับปุ่ม submit
8. **เพิ่ม Hidden Input Fields** - เพิ่มฟิลด์ที่ซ่อน (link_id, source, signature, timestamp, addr, language, phonecode)
9. **ทำความสะอาด Dialog** - ลบ prompt text และเพิ่ม `id="dialog-content"`
10. **เพิ่ม JavaScript Functionality** - เพิ่ม event handlers, encryption, และ form submission logic

## การใช้งาน (Usage)

### ข้อกำหนดเบื้องต้น (Requirements)
- Python 3.6+

### การรัน (Running)

```bash
cd /Users/lp-03/fxleader_modifile_html
python3 modify_html.py
```

### Output Example

```
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
  ✓ JavaScript functionality added

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
├── modify_html.py              # Python script หลัก
├── fxleader.md                 # คำสั่งการแก้ไข
├── README.md
└── example/
    ├── en/index.html          # English version (แก้ไขแล้ว)
    ├── lo/index.html          # Lao version (แก้ไขแล้ว)
    ├── ms/index.html          # Malay version (แก้ไขแล้ว)
    ├── th/index.html          # Thai version (แก้ไขแล้ว)
    └── vi/index.html          # Vietnamese version (แก้ไขแล้ว)
```

## Classes และ Methods

### HTMLModifier Class

ระบบใช้คลาส `HTMLModifier` ที่มี methods ต่อไปนี้:

- `add_google_tag()` - เพิ่ม Google Tag Manager
- `add_cloudflare_dependencies()` - เพิ่ม Cloudflare dependencies
- `convert_absolute_to_relative_paths()` - แปลง URLs
- `ensure_join_form_id()` - เพิ่ม form ID
- `add_country_select_onchange()` - เพิ่ม event handler
- `add_cloudflare_turnstile_component()` - เพิ่ม CAPTCHA
- `ensure_submit_button_id()` - เพิ่ม button ID
- `add_hidden_input_fields()` - เพิ่ม hidden fields
- `clean_dialog_and_add_id()` - ทำความสะอาด dialog
- `add_javascript_functionality()` - เพิ่ม JavaScript
- `apply_all_modifications()` - รัน all steps ตามลำดับ

## Technical Details

- **Language**: Python 3
- **Regex-based**: ใช้ regular expressions สำหรับการค้นหาและแทนที่
- **Idempotent**: สามารถรัน multiple times โดยไม่ทำให้ duplicate
- **Multi-language Support**: รองรับ 5 ภาษา (EN, LO, MS, TH, VI)

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
    <input type="hidden" value="fxleader" name="link_id">
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

## JavaScript Features

เจอที่เพิ่มเข้ามา:

- `countryChange()` - ฟังก์ชันสำหรับจัดการการเลือกประเทศ
- `dialog-open/dialog-close` - Event listeners สำหรับ dialog
- RSA + AES Encryption - เข้ารหัสข้อมูลฟอร์มก่อนส่ง
- Form Submission - POST ไปยัง `/website/register`

## Notes

- Idempotent design - สามารถรัน script หลายครั้งได้
- All modifications checked before applying (avoid duplicates)
- Support for multiple HTML structures
- Comprehensive error reporting

## Support

สำหรับความเห็นหรือปัญหา โปรดดูไฟล์ `fxleader.md` สำหรับข้อกำหนด
