### 資料庫字串變更
把 config.yml.sample 拷貝一份為 config.yml

針對一個資料庫中裡面所有的資料表的 varchar, text 欄位，做字串置換

---

**執行環境**

python 3.7

---

**使用方式**

1. 例如要將資料庫中所有 varchar, text 中的「韓語」置換成「韓國語」 
![image](https://drive.google.com/uc?export=view&id=14H-KIV6EhW3Gb-9iOpOl_jvEpg6yng7w)

2. 在 yaml 設定檔中設定舊字串和新字串
![image](https://drive.google.com/uc?export=view&id=1sagxinTymJIv18AJrPqNHmSjO212OcU8)

3. 執行轉換程式
![image](https://drive.google.com/uc?export=view&id=1VgfP7G7jdRTIKBdlv8nTLvy5LOSvRasj)

4. 成功將文字「韓語」置換成「韓國語」 
![image](https://drive.google.com/uc?export=view&id=1k4LlY272_I3LV7E-Jv8z-he7SJSWW8Tf)
