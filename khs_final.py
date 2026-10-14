# -*- coding: utf-8 -*-
"""
Khan Herbal Stores - Final WooCommerce CSV builder v4
- Product NAME in English (URL slug English)
- Urdu name only inside descriptions
- Random price + stock + low stock alert
- Add to Cart button visible
- WhatsApp "Place Order" button in every product description
- Companion khs_slug_fixer.php generated to fix any slug 404 issues
- Rank Math meta fields
- 5 keywords per product (short, long, nav, trans, comm)
"""
import csv, re, random
from collections import defaultdict
from urllib.parse import quote

STORE = "Khan Herbal Stores"
BASE  = "https://darkcyan-turkey-703045.hostingersite.com/product/"
WHATSAPP_NUMBER = "923218224219"          # admin WhatsApp (no +, no leading 00)
WHATSAPP_DISPLAY = "+92 321 8224219"

# ------------------------------------------------------------------
# MASTER LIST: slug|English|Urdu|Brand|Category|Subcategory
# ------------------------------------------------------------------
RAW = """
roghan-badam-qarshi|Almond Oil|روغن بادام|Qarshi|Oils|Herbal Oils
roghan-zaitoon-hamdard|Olive Oil|روغن زیتون|Hamdard|Oils|Herbal Oils
roghan-kalonji-ajmal|Black Seed Oil|روغن کلونجی|Ajmal|Oils|Herbal Oils
roghan-nariyal-ashraf-labs|Coconut Oil|روغن ناریل|Ashraf Labs|Oils|Herbal Oils
roghan-sarson-marhaba|Mustard Oil|روغن سرسوں|Marhaba|Oils|Herbal Oils
roghan-arand-tayyebi|Castor Oil|روغن ارنڈ|Tayyebi|Oils|Herbal Oils
roghan-til-herbion|Sesame Oil|روغن تل|Herbion|Oils|Herbal Oils
roghan-amla-noorani|Amla Oil|روغن آملہ|Noorani|Oils|Herbal Oils
roghan-neem-hashmi|Neem Oil|روغن نیم|Hashmi|Oils|Herbal Oils
roghan-lehsan-new-shama|Garlic Oil|روغن لہسن|New Shama|Oils|Herbal Oils
roghan-podina-sona-herbal|Mint Oil|روغن پودینہ|Sona Herbal|Oils|Herbal Oils
roghan-elaichi-al-shifa|Cardamom Oil|روغن الائچی|Al-Shifa|Oils|Herbal Oils
roghan-saunf-khan-herbal-multan|Fennel Oil|روغن سونف|Khan Herbal Multan|Oils|Herbal Oils
roghan-kaddu-swat-herbal|Pumpkin Seed Oil|روغن کدو|Swat Herbal|Oils|Herbal Oils
roghan-methi-baloch-herbal|Fenugreek Oil|روغن میتھی|Baloch Herbal|Oils|Herbal Oils
roghan-malkangni-herbiotics|Malkangni Oil|روغن مالکنگنی|Herbiotics|Oils|Herbal Oils
roghan-babchi-qarshi|Babchi Oil|روغن بابچی|Qarshi|Oils|Herbal Oils
roghan-chamomile-hamdard|Chamomile Oil|روغن کیمومائل|Hamdard|Oils|Herbal Oils
roghan-chanbeli-ajmal|Jasmine Oil|روغن چنبیلی|Ajmal|Oils|Herbal Oils
roghan-lemon-ashraf-labs|Lemon Oil|روغن لیموں|Ashraf Labs|Oils|Herbal Oils
roghan-eucalyptus-marhaba|Eucalyptus Oil|روغن یوکلپٹس|Marhaba|Oils|Herbal Oils
roghan-kewra-tayyebi|Kewra Oil|روغن کیوڑہ|Tayyebi|Oils|Herbal Oils
roghan-tea-tree-herbion|Tea Tree Oil|روغن ٹی ٹری|Herbion|Oils|Herbal Oils
roghan-mehndi-noorani|Henna Oil|روغن مہندی|Noorani|Oils|Herbal Oils
roghan-zaffran-hashmi|Saffron Oil|روغن زعفران|Hashmi|Oils|Herbal Oils
roghan-badam-kalonji-mix-new-shama|Almond & Black Seed Oil Mix|روغن بادام کلونجی مکس|New Shama|Oils|Herbal Oils
roghan-dhatura-sona-herbal|Datura Oil|روغن دھتورہ|Sona Herbal|Oils|Herbal Oils
roghan-baiza-murgh-al-shifa|Egg Yolk Oil|روغن بیضہ مرغ|Al-Shifa|Oils|Herbal Oils
roghan-khaskhash-khan-herbal-multan|Poppy Seed Oil|روغن خشخاش|Khan Herbal Multan|Oils|Herbal Oils
roghan-bhangra-swat-herbal|Bhringraj Oil|روغن بھنگرہ|Swat Herbal|Oils|Herbal Oils
majun-chob-chini|Majun Chob Chini|معجون چوب چینی||Majun, Khamira & Jawarish|Majun
majun-supari-pak|Majun Supari Pak|معجون سپاری پاک||Majun, Khamira & Jawarish|Majun
majun-khurma|Majun Khurma|معجون خرمہ||Majun, Khamira & Jawarish|Majun
majun-dabeed-ul-ward|Majun Dabeed ul Ward|معجون دبید الورد||Majun, Khamira & Jawarish|Majun
majun-falasifa|Majun Falasifa|معجون فلاسفہ||Majun, Khamira & Jawarish|Majun
majun-pamba-dana|Majun Pamba Dana|معجون پمبہ دانہ||Majun, Khamira & Jawarish|Majun
majun-sa-alab|Majun Sa'alab|معجون ثعلب||Majun, Khamira & Jawarish|Majun
majun-muqawwi|Majun Muqawwi|معجون مقوی||Majun, Khamira & Jawarish|Majun
majun-kundar|Majun Kundar|معجون کندر||Majun, Khamira & Jawarish|Majun
khamira-gauzaban|Khamira Gauzaban|خمیرہ گاؤزبان||Majun, Khamira & Jawarish|Khamira
khamira-abresham|Khamira Abresham|خمیرہ ابریشم||Majun, Khamira & Jawarish|Khamira
khamira-sandal|Khamira Sandal|خمیرہ صندل||Majun, Khamira & Jawarish|Khamira
khamira-banafsha|Khamira Banafsha|خمیرہ بنفشہ||Majun, Khamira & Jawarish|Khamira
itrifal-ustokhuddoos|Itrifal Ustokhuddoos|اطریفل اسطوخودوس||Majun, Khamira & Jawarish|Itrifal
itrifal-zamani|Itrifal Zamani|اطریفل زمانی||Majun, Khamira & Jawarish|Itrifal
itrifal-kishneez|Itrifal Kishneez|اطریفل کشنیزی||Majun, Khamira & Jawarish|Itrifal
itrifal-mulayyin|Itrifal Mulayyin|اطریفل ملین||Majun, Khamira & Jawarish|Itrifal
jawarish-anareen|Jawarish Anareen|جوارش انارین||Majun, Khamira & Jawarish|Jawarish
jawarish-jalinoos|Jawarish Jalinoos|جوارش جالینوس||Majun, Khamira & Jawarish|Jawarish
jawarish-shahi|Jawarish Shahi|جوارش شاہی||Majun, Khamira & Jawarish|Jawarish
jawarish-amla|Jawarish Amla|جوارش آملہ||Majun, Khamira & Jawarish|Jawarish
jawarish-kamooni|Jawarish Kamooni|جوارش کمونی||Majun, Khamira & Jawarish|Jawarish
jawarish-ood-sheerin|Jawarish Ood Sheerin|جوارش عود شیریں||Majun, Khamira & Jawarish|Jawarish
jawarish-halila|Jawarish Halila|جوارش ہلیلہ||Majun, Khamira & Jawarish|Jawarish
laboob-kabir|Laboob Kabir|لبوب کبیر||Majun, Khamira & Jawarish|Laboob
laboob-sagheer|Laboob Sagheer|لبوب صغیر||Majun, Khamira & Jawarish|Laboob
majun-surinjan|Majun Surinjan|معجون سورنجان||Majun, Khamira & Jawarish|Majun
majun-brahmi|Majun Brahmi|معجون برہمی||Majun, Khamira & Jawarish|Majun
majun-ushba|Majun Ushba|معجون عشبہ||Majun, Khamira & Jawarish|Majun
majun-azraqi|Majun Azraqi|معجون ازراقی||Majun, Khamira & Jawarish|Majun
majun-najah|Majun Najah|معجون نجاح||Majun, Khamira & Jawarish|Majun
khamira-marwareed|Khamira Marwareed|خمیرہ مروارید||Majun, Khamira & Jawarish|Khamira
jawarish-zarooni|Jawarish Zarooni|جوارش زرعونی||Majun, Khamira & Jawarish|Jawarish
jawarish-shahi-special|Jawarish Shahi Special|جوارش شاہی سپیشل||Majun, Khamira & Jawarish|Jawarish
majun-muqawwi-reham|Majun Muqawwi Reham|معجون مقوی رحم||Majun, Khamira & Jawarish|Majun
sharbat-toot-siyah|Mulberry Syrup|شربت توت سیاہ||Syrups|Herbal Syrups
sharbat-anar|Pomegranate Syrup|شربت انار||Syrups|Herbal Syrups
sharbat-sandal|Sandalwood Syrup|شربت صندل||Syrups|Herbal Syrups
sharbat-banafsha|Violet Syrup|شربت بنفشہ||Syrups|Herbal Syrups
sharbat-khaskhash|Poppy Seed Syrup|شربت خشخاش||Syrups|Herbal Syrups
sharbat-bazoori|Bazoori Syrup|شربت بزوری||Syrups|Herbal Syrups
sharbat-faulad|Fauld Syrup|شربت فولاد||Syrups|Herbal Syrups
sharbat-zaffran|Saffron Syrup|شربت زعفران||Syrups|Herbal Syrups
sharbat-tulsi|Tulsi Syrup|شربت تلسی||Syrups|Herbal Syrups
sharbat-unab|Jujube Syrup|شربت عناب||Syrups|Herbal Syrups
sharbat-sapistan|Sapistan Syrup|شربت سپستان||Syrups|Herbal Syrups
sharbat-bel-giri|Wood Apple Syrup|شربت بیل گری||Syrups|Herbal Syrups
sharbat-fuad|Fuad Syrup|شربت فؤاد||Syrups|Herbal Syrups
sharbat-lemon|Lemon Syrup|شربت لیموں||Syrups|Herbal Syrups
sharbat-orange|Orange Syrup|شربت اورنج||Syrups|Herbal Syrups
sharbat-seb|Apple Syrup|شربت سیب||Syrups|Herbal Syrups
sharbat-angoor|Grape Syrup|شربت انگور||Syrups|Herbal Syrups
sharbat-julab|Julab Syrup|شربت جلاب||Syrups|Herbal Syrups
sharbat-bazoori-motadil|Bazoori Motadil Syrup|شربت بزوری معتدل||Syrups|Herbal Syrups
sharbat-kewra|Kewra Syrup|شربت کیوڑہ||Syrups|Herbal Syrups
sharbat-gulab|Rose Syrup|شربت گلاب||Syrups|Herbal Syrups
sharbat-podina|Mint Syrup|شربت پودینہ||Syrups|Herbal Syrups
sharbat-chirayata|Chirayata Syrup|شربت چرائتہ||Syrups|Herbal Syrups
sharbat-shahatra|Shahatra Syrup|شربت شاہترہ||Syrups|Herbal Syrups
sharbat-mulethi|Mulethi Syrup|شربت ملٹھی||Syrups|Herbal Syrups
sharbat-aloe-vera|Aloe Vera Syrup|شربت ایلوویرا||Syrups|Herbal Syrups
sharbat-imli|Tamarind Syrup|شربت املی||Syrups|Herbal Syrups
sharbat-eucalyptus|Eucalyptus Syrup|شربت یوکلپٹس||Syrups|Herbal Syrups
sharbat-halaq|Throat Syrup|شربت حلق||Syrups|Herbal Syrups
sharbat-jigar|Jigar Syrup|شربت جگر||Syrups|Herbal Syrups
sharbat-bachon-ka-tonic|Children's Tonic Syrup|شربت بچوں کا ٹانک||Syrups|Herbal Syrups
sharbat-chamomile|Chamomile Syrup|شربت کیمومائل||Syrups|Herbal Syrups
sharbat-amla-murabba|Amla Murabba Syrup|شربت آملہ مربہ||Syrups|Herbal Syrups
sharbat-habshi|Habshi Syrup|شربت حبشی||Syrups|Herbal Syrups
sharbat-dinar|Dinar Syrup|شربت دینار||Syrups|Herbal Syrups
sharbat-ejaz|Ejaz Syrup|شربت اعجاز||Syrups|Herbal Syrups
sharbat-mufarrah|Mufarrah Syrup|شربت مفرح||Syrups|Herbal Syrups
sharbat-injibar|Injibar Syrup|شربت انجبار||Syrups|Herbal Syrups
sharbat-araq-mako|Mako Araq Syrup|شربت عرق مکو||Syrups|Herbal Syrups
sharbat-araq-kasni|Kasni Araq Syrup|شربت عرق کاسنی||Syrups|Herbal Syrups
sirka-seb|Apple Cider Vinegar|سرکہ سیب||Vinegars|Herbal Vinegars
sirka-jaman|Jaman Vinegar|سرکہ جامن||Vinegars|Herbal Vinegars
sirka-angoor|Grape Vinegar|سرکہ انگور||Vinegars|Herbal Vinegars
sirka-anar|Pomegranate Vinegar|سرکہ انار||Vinegars|Herbal Vinegars
sirka-lemon|Lemon Vinegar|سرکہ لیموں||Vinegars|Herbal Vinegars
sirka-kalonji|Black Seed Vinegar|سرکہ کلونجی||Vinegars|Herbal Vinegars
sirka-ajwain|Carom Seed Vinegar|سرکہ اجوائن||Vinegars|Herbal Vinegars
sirka-adrak|Ginger Vinegar|سرکہ ادرک||Vinegars|Herbal Vinegars
sirka-lehsan|Garlic Vinegar|سرکہ لہسن||Vinegars|Herbal Vinegars
sirka-pyaz|Onion Vinegar|سرکہ پیاز||Vinegars|Herbal Vinegars
sirka-alsi|Flaxseed Vinegar|سرکہ السی||Vinegars|Herbal Vinegars
sirka-safaid|White Vinegar|سرکہ سفید||Vinegars|Herbal Vinegars
sirka-ganna|Sugarcane Vinegar|سرکہ گنا||Vinegars|Herbal Vinegars
sirka-kishmish|Raisin Vinegar|سرکہ کشمش||Vinegars|Herbal Vinegars
sirka-shahad|Honey Vinegar|سرکہ شہد||Vinegars|Herbal Vinegars
sirka-sangtra|Orange Vinegar|سرکہ سنگترہ||Vinegars|Herbal Vinegars
sirka-imli|Tamarind Vinegar|سرکہ املی||Vinegars|Herbal Vinegars
sirka-falsa|Falsa Vinegar|سرکہ فالسہ||Vinegars|Herbal Vinegars
sirka-loquat|Loquat Vinegar|سرکہ لوکاٹ||Vinegars|Herbal Vinegars
sirka-aloo-bukhara|Plum Vinegar|سرکہ آلو بخارہ||Vinegars|Herbal Vinegars
sirka-seb-moringa|Apple Moringa Vinegar|سرکہ سیب مورنگا||Vinegars|Herbal Vinegars
sirka-jaman-kalonji|Jaman Black Seed Vinegar|سرکہ جامن کلونجی||Vinegars|Herbal Vinegars
sirka-5in1-mix|5-in-1 Mixed Vinegar|سرکہ 5in1 مکس||Vinegars|Herbal Vinegars
sirka-kalonji-shahad|Black Seed Honey Vinegar|سرکہ کلونجی شہد||Vinegars|Herbal Vinegars
sirka-ajwain-kalonji|Carom Black Seed Vinegar|سرکہ اجوائن کلونجی||Vinegars|Herbal Vinegars
sirka-seb-lehsan|Apple Garlic Vinegar|سرکہ سیب لہسن||Vinegars|Herbal Vinegars
kalonji|Kalonji (Black Seed)|کلونجی||Herbs & Botanicals|Seeds
tukhm-malinga|Malinga Seeds|تخم ملنگا||Herbs & Botanicals|Seeds
ispaghol-chilka|Psyllium Husk|اسپغول چھلکا||Herbs & Botanicals|Seeds
alsi-beej|Flaxseed (Alsi)|السی بیج||Herbs & Botanicals|Seeds
methi-dana|Fenugreek Seeds|میتھی دانہ||Herbs & Botanicals|Seeds
ajwain-desi|Carom Seeds (Ajwain)|اجوائن دیسی||Herbs & Botanicals|Seeds
saunf|Fennel Seeds (Saunf)|سونف||Herbs & Botanicals|Seeds
zeera-safaid|White Cumin|زیرہ سفید||Herbs & Botanicals|Seeds
zeera-siyah|Black Cumin|زیرہ سیاہ||Herbs & Botanicals|Seeds
dhania-khushk|Dried Coriander|دھنیا خشک||Herbs & Botanicals|Seeds
tukhm-kasni|Chicory Seeds|تخم کاسنی||Herbs & Botanicals|Seeds
tukhm-kaddu|Pumpkin Seeds|تخم کدو||Herbs & Botanicals|Seeds
tukhm-khaskhash|Poppy Seeds|تخم خشخاش||Herbs & Botanicals|Seeds
tukhm-hina|Henna Seeds|تخم حنا||Herbs & Botanicals|Seeds
sarson-dana|Mustard Seeds (Sarson Dana)|سرسوں دانہ||Herbs & Botanicals|Seeds
chia-seed|Chia Seeds|چیا سیڈ||Herbs & Botanicals|Seeds
tukhm-rehan|Basil Seeds|تخم ریحان||Herbs & Botanicals|Seeds
til-siyah|Black Sesame Seeds|تل سیاہ||Herbs & Botanicals|Seeds
til-safaid|White Sesame Seeds|تل سفید||Herbs & Botanicals|Seeds
tukhm-bhang|Hemp Seeds|تخم بھنگ||Herbs & Botanicals|Seeds
tukhm-balanga|Balanga Seeds|تخم بالنگا||Herbs & Botanicals|Seeds
tukhm-katan|Linseed|تخم کتان||Herbs & Botanicals|Seeds
tukhm-mooli|Radish Seeds|تخم مولی||Herbs & Botanicals|Seeds
tukhm-shaljam|Turnip Seeds|تخم شلجم||Herbs & Botanicals|Seeds
tukhm-pyaz|Onion Seeds|تخم پیاز||Herbs & Botanicals|Seeds
tukhm-gajar|Carrot Seeds|تخم گاجر||Herbs & Botanicals|Seeds
tukhm-kharbuza|Muskmelon Seeds|تخم خربوزہ||Herbs & Botanicals|Seeds
tukhm-tarbooz|Watermelon Seeds|تخم تربوز||Herbs & Botanicals|Seeds
tukhm-khayareen|Cucumber Seeds|تخم خیارین||Herbs & Botanicals|Seeds
tukhm-kharfa|Kharfa Seeds|تخم خرفہ||Herbs & Botanicals|Seeds
tukhm-mako|Mako Seeds|تخم مکو||Herbs & Botanicals|Seeds
tukhm-bakain|Bakain Seeds|تخم بکائن||Herbs & Botanicals|Seeds
tukhm-kunjad|Sesame Seeds|تخم کنجد||Herbs & Botanicals|Seeds
tukhm-jarjeer|Garden Cress Seeds|تخم جرجیر||Herbs & Botanicals|Seeds
tukhm-losan|Losan Seeds|تخم لوسن||Herbs & Botanicals|Seeds
rai-dana|Rai Dana|رائی دانہ||Herbs & Botanicals|Seeds
methray|Methray|میتھرے||Herbs & Botanicals|Seeds
jo-khar|Barley Salt|جو کھار||Herbs & Botanicals|Minerals
tukhm-ispand|Ispand Seeds|تخم اسپند||Herbs & Botanicals|Seeds
tukhm-harmal|Harmal Seeds|تخم حرمل||Herbs & Botanicals|Seeds
tukhm-sars|Mustard Seeds (Tukhm Sars)|تخم سرس||Herbs & Botanicals|Seeds
tukhm-neem|Neem Seeds|تخم نیم||Herbs & Botanicals|Seeds
tukhm-bargad|Banyan Seeds|تخم برگد||Herbs & Botanicals|Seeds
tukhm-peepal|Peepal Seeds|تخم پیپل||Herbs & Botanicals|Seeds
indrayan-tukhm|Indrayan Seeds|اندرائن تخم||Herbs & Botanicals|Seeds
jamal-gota-beej|Jamal Gota Seeds|جمال گوٹہ بیج||Herbs & Botanicals|Seeds
amaltas-beej|Amaltas Seeds|املتاس بیج||Herbs & Botanicals|Seeds
dhatura-beej|Datura Seeds|دھتورہ بیج||Herbs & Botanicals|Seeds
behi-dana|Behi Dana|بہی دانہ||Herbs & Botanicals|Seeds
babchi-beej|Babchi Seeds|بابچی بیج||Herbs & Botanicals|Seeds
tukhm-karafs|Celery Seeds|تخم کرفس||Herbs & Botanicals|Seeds
tukhm-gandana|Gandana Seeds|تخم گندنا||Herbs & Botanicals|Seeds
tukhm-shahi|Tukhm Shahi|تخم شاہی||Herbs & Botanicals|Seeds
mulethi|Mulethi (Liquorice)|ملٹھی||Herbs & Botanicals|Roots
ashwagandha|Ashwagandha|اشوگندھا||Herbs & Botanicals|Roots
dalchini|Cinnamon|دارچینی||Herbs & Botanicals|Spices
chob-chini|Chob Chini|چوب چینی||Herbs & Botanicals|Roots
aqarqarha|Aqarqarha|عقرقرحا||Herbs & Botanicals|Roots
behman-safaid|Behman Safaid|بہمن سفید||Herbs & Botanicals|Roots
behman-surkh|Behman Surkh|بہمن سرخ||Herbs & Botanicals|Roots
kholanjan|Kholanjan|خولنجان||Herbs & Botanicals|Roots
sonth|Sonth (Dried Ginger)|سونٹھ||Herbs & Botanicals|Spices
haldi|Turmeric|ہلدی||Herbs & Botanicals|Spices
musli-safaid|Musli Safaid|موصلی سفید||Herbs & Botanicals|Roots
musli-siyah|Musli Siyah|موصلی سیاہ||Herbs & Botanicals|Roots
satavar|Satavar|ستاور||Herbs & Botanicals|Roots
gond-katira|Gond Katira|گوند کتیرا||Herbs & Botanicals|Gums
gond-kikar|Gond Kikar|گوند کیکر||Herbs & Botanicals|Gums
gond-babool|Gond Babool|گوند ببول||Herbs & Botanicals|Gums
hing-khalis|Hing (Asafoetida)|ہنگ خالص||Herbs & Botanicals|Gums
loban|Loban|لوبان||Herbs & Botanicals|Gums
kundar|Kundar|کندر||Herbs & Botanicals|Gums
murr|Murr (Myrrh)|مر||Herbs & Botanicals|Gums
shilajit-khalis|Shilajit|سلاجیت خالص||Herbs & Botanicals|Gums
kafoor|Kafoor (Camphor)|کافور||Herbs & Botanicals|Minerals
amla-khushk|Dried Amla|آملہ خشک||Herbs & Botanicals|Dried Fruits
halila-siyah|Halila Siyah|ہلیلہ سیاہ||Herbs & Botanicals|Dried Fruits
halila-zard|Halila Zard|ہلیلہ زرد||Herbs & Botanicals|Dried Fruits
bahera|Bahera|بہیڑہ||Herbs & Botanicals|Dried Fruits
baleela|Baleela|بلیلہ||Herbs & Botanicals|Dried Fruits
zarshak|Zarshak|زرشک||Herbs & Botanicals|Dried Fruits
unab|Unab (Jujube)|عناب||Herbs & Botanicals|Dried Fruits
sapistan|Sapistan|سپستان||Herbs & Botanicals|Dried Fruits
chirayata|Chirayata|چرائتہ||Herbs & Botanicals|Whole Herbs
chaksu|Chaksu|چاکسو||Herbs & Botanicals|Seeds
indar-jau|Indar Jau|اندر جو||Herbs & Botanicals|Whole Herbs
gul-madar-jar|Gul Madar Root|گل مدار جڑ||Herbs & Botanicals|Roots
bakhra|Bakhra|بکھڑا||Herbs & Botanicals|Whole Herbs
giloe|Giloe (Giloy)|گلو||Herbs & Botanicals|Whole Herbs
peepal-jar|Peepal Root|پیپل جڑ||Herbs & Botanicals|Roots
peepal-mool|Peepal Mool|پیپلامول||Herbs & Botanicals|Roots
taj|Taj (Cassia)|تج||Herbs & Botanicals|Spices
kachur|Kachur|کچور||Herbs & Botanicals|Roots
jatamansi|Jatamansi|جٹامانسی||Herbs & Botanicals|Roots
balchar|Balchar|بالچھڑ||Herbs & Botanicals|Roots
nagar-motha|Nagar Motha|ناگر موتھا||Herbs & Botanicals|Roots
dhamasa-boti|Dhamasa Herb|دھماسہ بوٹی||Herbs & Botanicals|Whole Herbs
chhirila|Chhirila|چھڑیلہ||Herbs & Botanicals|Whole Herbs
gorkh-pan|Gorkh Pan|گورکھ پان||Herbs & Botanicals|Whole Herbs
bargad-chhaal|Bargad Bark|برگد چھال||Herbs & Botanicals|Barks
kikar-chhaal|Kikar Bark|کیکر چھال||Herbs & Botanicals|Barks
neem-chhaal|Neem Bark|نیم چھال||Herbs & Botanicals|Barks
arjun-chhaal|Arjun Bark|ارجن چھال||Herbs & Botanicals|Barks
dar-hald|Dar Hald|دار ہلد||Herbs & Botanicals|Roots
mundi-boti|Mundi Herb|منڈی بوٹی||Herbs & Botanicals|Whole Herbs
chirchita|Chirchita|چرچٹہ||Herbs & Botanicals|Whole Herbs
sahjan-jar|Sahjan Root (Moringa)|سہانجنہ جڑ||Herbs & Botanicals|Roots
karanjwa|Karanjwa|کرنجوہ||Herbs & Botanicals|Seeds
gulab-phool|Rose Petals|گلاب پھول||Herbs & Botanicals|Flowers
gul-banafsha|Violet Flowers|گل بنفشہ||Herbs & Botanicals|Flowers
gul-nilofar|Blue Lotus Flowers|گل نیلوفر||Herbs & Botanicals|Flowers
gul-dhawa|Dhawa Flowers|گل دھاوا||Herbs & Botanicals|Flowers
gul-gauzaban|Gauzaban Flowers|گل گاؤزبان||Herbs & Botanicals|Flowers
gul-khera|Khera Flowers|گل خیرا||Herbs & Botanicals|Flowers
gul-abbas|Abbas Flowers|گل عباس||Herbs & Botanicals|Flowers
gul-babuna|Chamomile Flowers|گل بابونہ||Herbs & Botanicals|Flowers
gul-babool|Babool Flowers|گل ببول||Herbs & Botanicals|Flowers
gul-anar|Pomegranate Flowers|گل انار||Herbs & Botanicals|Flowers
gul-kesu|Kesu Flowers|گل کیسو||Herbs & Botanicals|Flowers
barg-hina|Henna Leaves|برگ حنا||Herbs & Botanicals|Leaves
barg-sudab|Rue Leaves|برگ سداب||Herbs & Botanicals|Leaves
barg-neem|Neem Leaves|برگ نیم||Herbs & Botanicals|Leaves
barg-bansa|Bansa Leaves|برگ بانسہ||Herbs & Botanicals|Leaves
barg-madar|Madar Leaves|برگ مدار||Herbs & Botanicals|Leaves
barg-beri|Beri Leaves|برگ بیری||Herbs & Botanicals|Leaves
barg-mehndi|Mehndi Leaves|برگ مہندی||Herbs & Botanicals|Leaves
barg-tulsi|Tulsi Leaves|برگ تلسی||Herbs & Botanicals|Leaves
barg-podina|Mint Leaves|برگ پودینہ||Herbs & Botanicals|Leaves
sanna-makki|Senna|سنا مکی||Herbs & Botanicals|Leaves
bhangra-siyah|Black Bhringraj|بھنگرہ سیاہ||Herbs & Botanicals|Whole Herbs
bhangra-safaid|White Bhringraj|بھنگرہ سفید||Herbs & Botanicals|Whole Herbs
shahatra|Shahatra (Fumitory)|شاہترہ||Herbs & Botanicals|Whole Herbs
kasni-boti|Kasni (Chicory)|کاسنی بوٹی||Herbs & Botanicals|Whole Herbs
mako-boti|Mako Herb|مکو بوٹی||Herbs & Botanicals|Whole Herbs
badiyan-khatai|Star Anise|بادیان خطائی||Herbs & Botanicals|Spices
sabz-elaichi|Green Cardamom|سبز الائچی||Herbs & Botanicals|Spices
bari-elaichi|Black Cardamom|بڑی الائچی||Herbs & Botanicals|Spices
laung|Cloves|لونگ||Herbs & Botanicals|Spices
jaifal|Nutmeg|جائفل||Herbs & Botanicals|Spices
jawitri|Mace|جاوتری||Herbs & Botanicals|Spices
kali-mirch|Black Pepper|کالی مرچ||Herbs & Botanicals|Spices
safaid-mirch|White Pepper|سفید مرچ||Herbs & Botanicals|Spices
dar-filfil|Long Pepper|دار فلفل||Herbs & Botanicals|Spices
zaffran|Saffron|زعفران||Herbs & Botanicals|Spices
tabasheer|Tabasheer|طباشیر||Herbs & Botanicals|Minerals
elaichi-khurd|Small Cardamom|الائچی خورد||Herbs & Botanicals|Spices
elaichi-kalan|Large Cardamom|الائچی کلاں||Herbs & Botanicals|Spices
mastagi-roomi|Mastic|مصطگی رومی||Herbs & Botanicals|Gums
ood-hindi|Indian Agarwood|عود ہندی||Herbs & Botanicals|Minerals
sandal-safaid|White Sandalwood|صندل سفید||Herbs & Botanicals|Minerals
sandal-surkh|Red Sandalwood|صندل سرخ||Herbs & Botanicals|Minerals
agar|Agarwood|اگر||Herbs & Botanicals|Minerals
jadwar-khatai|Jadwar Khatai|جدوار خطائی||Herbs & Botanicals|Roots
zarnabad|Zarnabad|زرنباد||Herbs & Botanicals|Spices
qaranfal|Qaranfal (Cloves)|قرنفل||Herbs & Botanicals|Spices
saad-kufi|Saad Kufi|سعد کوفی||Herbs & Botanicals|Roots
asgandh|Asgandh|اسگندھ||Herbs & Botanicals|Roots
tudri-surkh|Red Tudri|تودری سرخ||Herbs & Botanicals|Seeds
tudri-safaid|White Tudri|تودری سفید||Herbs & Botanicals|Seeds
basfaij|Basfaij|بسفائج||Herbs & Botanicals|Whole Herbs
aftimoon|Aftimoon|افتیمون||Herbs & Botanicals|Whole Herbs
marwareed|Pearl|مروارید||Herbs & Botanicals|Minerals
marjan|Coral|مرجان||Herbs & Botanicals|Minerals
hajar-ul-yahood|Hajar ul Yahood|حجر الیہود||Herbs & Botanicals|Minerals
sang-jarahat|Sang Jarahat|سنگ جراحت||Herbs & Botanicals|Minerals
noshadar|Noshadar|نوشادر||Herbs & Botanicals|Minerals
qalmi-shora|Qalmi Shora|قلمی شورہ||Herbs & Botanicals|Minerals
gandhak-amla-sar|Gandhak Amla Sar|گندھک آملہ سار||Herbs & Botanicals|Minerals
neela-thotha|Neela Thotha|نیلا تھوتھا||Herbs & Botanicals|Minerals
sohaga|Sohaga (Borax)|سہاگہ||Herbs & Botanicals|Minerals
phitkari|Phitkari (Alum)|پھٹکڑی||Herbs & Botanicals|Minerals
samundar-jhaag|Samundar Jhaag|سمندر جھاگ||Herbs & Botanicals|Minerals
revand-chini|Revand Chini|ریوند چینی||Herbs & Botanicals|Roots
halila-kabuli|Halila Kabuli|ہلیلہ کابلی||Herbs & Botanicals|Dried Fruits
gul-surkh|Gul Surkh (Red Rose)|گل سرخ||Herbs & Botanicals|Flowers
safoof-hazim|Safoof Hazim|سفوف ہاضم||Safoof, Kushta & Hab|Safoof
safoof-mulayyin|Safoof Mulayyin|سفوف ملین||Safoof, Kushta & Hab|Safoof
safoof-mughalliz|Safoof Mughalliz|سفوف مغلظ||Safoof, Kushta & Hab|Safoof
safoof-jiryan|Safoof Jiryan|سفوف جریان||Safoof, Kushta & Hab|Safoof
safoof-tabkheer|Safoof Tabkheer|سفوف تبخیر||Safoof, Kushta & Hab|Safoof
safoof-ustokhuddoos|Safoof Ustokhuddoos|سفوف اسطوخودوس||Safoof, Kushta & Hab|Safoof
safoof-sual|Safoof Sual|سفوف سعال||Safoof, Kushta & Hab|Safoof
safoof-kamar-kas|Safoof Kamar Kas|سفوف کمر کس||Safoof, Kushta & Hab|Safoof
safoof-sa-alab-misri|Safoof Sa'alab Misri|سفوف ثعلب مصری||Safoof, Kushta & Hab|Safoof
kushta-faulad|Kushta Fauld|کشتہ فولاد||Safoof, Kushta & Hab|Kushta
kushta-jist|Kushta Jist|کشتہ جست||Safoof, Kushta & Hab|Kushta
kushta-marjan|Kushta Marjan|کشتہ مرجان||Safoof, Kushta & Hab|Kushta
kushta-shangarf|Kushta Shangarf|کشتہ شنگرف||Safoof, Kushta & Hab|Kushta
hab-kabid-noshadari|Hab Kabid Noshadari|حب کبد نوشادری||Safoof, Kushta & Hab|Hab
hab-tankar|Hab Tankar|حب تنکار||Safoof, Kushta & Hab|Hab
majun-sohaga|Majun Sohaga|معجون سہاگہ||Safoof, Kushta & Hab|Majun
itrifal-muqal|Itrifal Muqal|اطریفل مقل||Safoof, Kushta & Hab|Itrifal
safoof-chatni|Safoof Chatni|سفوف چٹنی||Safoof, Kushta & Hab|Safoof
hab-ustokhuddoos|Hab Ustokhuddoos|حب اسطوخودوس||Safoof, Kushta & Hab|Hab
"""

P = [r.split('|') for r in RAW.strip().split('\n')]
assert len(P) == 325, f"Expected 325 products, got {len(P)}"
for r in P:
    assert len(r) == 6, f"Bad row (needs 6 fields): {r}"

# ------------------------------------------------------------------
# KEYWORD BUILDER
# ------------------------------------------------------------------
def build_keywords(en, brand, cat):
    n = en.lower()
    short    = n
    long_t   = f"buy {n} online in pakistan"
    nav      = f"{brand} {n}".lower() if brand else f"{n} price in pakistan"
    trans    = f"buy {n} online"
    comm     = f"best {n} in pakistan"
    return short, [long_t, nav, trans, comm]

# ------------------------------------------------------------------
# RANDOM PRICE + STOCK
# ------------------------------------------------------------------
PRICE_RANGES = {
    "Oils": (450, 1400),
    "Syrups": (350, 1000),
    "Vinegars": (400, 900),
    "Majun, Khamira & Jawarish": (500, 1800),
    "Herbs & Botanicals": (150, 850),
    "Safoof, Kushta & Hab": (350, 1500),
}

def random_price(i):
    rng = random.Random(1000 + i)
    lo, hi = PRICE_RANGES.get(P[i][4], (250, 900))
    p = rng.randint(lo, hi)
    return (p // 50) * 50

def random_stock(i):
    rng = random.Random(2000 + i)
    return rng.randint(20, 80)

LOW_STOCK_ALERT = 5

# ------------------------------------------------------------------
# CATEGORY-LEVEL ABOUT
# ------------------------------------------------------------------
CAT_ABOUT = {
    "Oils": (
        "Herbal and seed oils are among the oldest and most versatile items in traditional "
        "Pakistani care. They are typically pressed from seeds, nuts, roots, flowers or leaves, "
        "and are used both topically and, in some cases, in cooking. The category includes light "
        "oils used for daily hair routines, richer oils for massage, and aromatic oils that are "
        "valued mainly for their scent. Storage matters: most traditional oils are best kept in a "
        "cool, dark place, away from direct sunlight, and capped tightly after each use. In "
        "{store}'s {sub} sub-category you will find oils sorted by their traditional source, which "
        "makes it easy to compare similar items at a glance."
    ),
    "Syrups": (
        "Syrups (sharbat) are a well-established part of traditional Pakistani herbal practice. "
        "They are typically prepared by combining herbal ingredients with sugar, honey or another "
        "sweet base, which gives them a longer shelf life and a pleasant taste. Traditional syrups "
        "are stored in cool, dry conditions and are commonly diluted before use. In our {store} "
        "catalogue, the syrups range sits under {sub}, and many customers prefer to build a small "
        "collection rather than buying a single bottle, since different syrups suit different parts "
        "of a household routine. This page gives you a factual overview of the product type without "
        "making any health claims."
    ),
    "Vinegars": (
        "Traditional vinegars (sirka) have been used in Pakistani kitchens and herbal practice for "
        "centuries. They are produced by fermenting fruit, honey, sugarcane or herbal infusions, and "
        "they range in colour and aroma depending on the base ingredient. Culinary vinegars are used "
        "in cooking and dressings, while traditional herbal vinegars are kept as part of a wellness "
        "shelf. Because vinegar is acidic, it is best stored in glass or food-grade containers, kept "
        "away from direct sunlight and used within its stated shelf life. In our {sub} group, you can "
        "compare different herbal vinegars side by side before ordering."
    ),
    "Majun, Khamira & Jawarish": (
        "Majun, khamira, itrifal, jawarish and laboob are classic categories of traditional Unani "
        "preparations used in Pakistan for generations. They are typically made from a mixture of "
        "herbs, spices, dried fruits, honey or sugar, and are usually taken in measured small "
        "quantities as part of a daily routine. Because they are concentrated, they are stored in "
        "airtight containers, kept cool and dry, and treated as part of a traditional practice rather "
        "than a modern supplement. The {sub} section of our {store} catalogue brings these "
        "preparations together so that customers can compare related items easily."
    ),
    "Herbs & Botanicals": (
        "Herbs, seeds, roots, barks, flowers, gums and traditional minerals form the backbone of "
        "Pakistani herbal practice. They are used in cooking, in traditional preparations and as "
        "ingredients in home remedies, and they vary widely in texture, aroma and how they are "
        "stored. Whole spices and seeds are best kept airtight, away from heat and moisture, while "
        "flowers and leaves lose aroma more quickly and are usually replaced more often. In our {sub} "
        "sub-category at {store}, you will find these items organised by their traditional form so "
        "that you can shop confidently."
    ),
    "Safoof, Kushta & Hab": (
        "Safoof, kushta, hab and traditional compound preparations are concentrated forms used in "
        "classical Unani practice. Safoof are powdered blends, kushta are prepared mineral or "
        "metallic compounds made through traditional processes, hab are pill-form preparations, and "
        "compounds such as majun and itrifal combine multiple ingredients. They are stored in "
        "airtight containers away from moisture and heat. Because these categories are traditional "
        "and concentrated, they are usually taken in small measured amounts as part of a routine, and "
        "are kept as part of a family's traditional shelf. This listing gives a general overview "
        "without any medical claims."
    ),
}

# ------------------------------------------------------------------
# NARRATIVE BLOCKS
# ------------------------------------------------------------------
INTRO = [
    "Finding a trustworthy {en} in Pakistan does not have to be complicated. At {store}, we curate traditional herbal products that Pakistani households have relied on for generations, and this {en} sits comfortably within that collection. Whether you are continuing a family routine or exploring herbal care for the first time, this product has been selected for its place within the {cat} section of our catalogue, alongside comparable items such as {l1} and {l2}. Below you will find clear, practical information about what this product is, how it is traditionally used in Pakistan, and how it relates to the rest of our herbal range. Every claim on this page is phrased in general, traditional-wellness language.",
    "At {store} we stock a broad range of traditional Pakistani herbal products, and this {en} is one of the items our regular customers ask for again and again. It belongs to our {cat} collection, in the same family as {l1} and {l2}, and is offered here with straightforward, factual information rather than exaggerated promises. If you are comparing options, this page explains the product type, its traditional context, its typical place in an everyday routine, and the related products you may want to consider. Our aim is to help you buy with confidence from a Pakistani herbal store that values clarity over hype.",
    "Traditional herbal products remain an important part of daily life in Pakistan, and this {en} is a familiar example. {store} offers it as part of the {cat} range, next to items such as {l1} and {l2}. This page is designed to answer the questions most customers have before ordering: what the product actually is, how it is generally used in traditional practice, what it is not, and which other items from our shelves are commonly purchased alongside it. We keep our language factual and avoid any medical, disease or cure claims.",
    "Whether you are building a traditional herbal shelf at home or topping up an item you already use, this {en} from {store} is a sensible choice. It belongs to the {cat} group in our store and shares its space with other popular products such as {l1} and {l2}. On this page you will find a practical overview written for real buyers in Pakistan, including information about its traditional role, the general way it is stored and handled, and the related items our customers often order together. We have deliberately kept the tone informative rather than promotional.",
    "This {en} is part of the {cat} selection at {store}, our Pakistani herbal store. It is offered with the same approach we apply to every listing: plain language, honest description and no unsupported health claims. Many of our customers buy it alongside {l1} and {l2}, which belong to the same family of traditional preparations. Read on for a detailed overview covering what the product is, the traditional context in which it is used in Pakistan, and how it links to the rest of our herbal catalogue.",
]

TRADITIONAL = [
    "In traditional Pakistani practice, {en} is generally understood within the wider context of {cat} rather than as a stand-alone item. Households often keep it alongside similar preparations and use it as part of a regular routine that has been passed down through generations. Traditional use is about consistency and appropriateness rather than intensity; small, regular use is normally preferred to occasional large use. Any guidance on quantity should come from the product label, and if you are unsure about suitability, it is always sensible to speak with a qualified practitioner before starting.",
    "Traditional use of {en} in Pakistan is often tied to particular times of day, seasons or life stages. It is commonly grouped with other items from the {cat} family so that a household can easily maintain a coherent routine. Traditional practice places strong emphasis on quality of ingredients, correct storage and knowing when a product suits you and when it does not. Because individual needs differ, we do not make universal recommendations; instead, we suggest reading the product label and, if you have any concern, consulting a qualified practitioner.",
    "In classical Unani and traditional herbal practice, {en} is treated as part of a broader system rather than an isolated product. This means that traditional users tend to combine it thoughtfully with related items such as {l1} and {l2} rather than using it in isolation. Long-term, consistent, moderate use is the traditional approach. Storage in a cool, dry place and clean handling also matter, because quality degrades quickly when traditional products are exposed to heat and moisture. Any specific dosage or duration should come from the label or a qualified practitioner.",
    "Traditional households in Pakistan often keep a small collection of {cat} items so that they can adapt to different times of the year. {en} fits naturally into this collection, and it is frequently placed next to items such as {l1} and {l2}. The emphasis in traditional practice is on appropriate use, quality sourcing, and knowing when to use which product. We describe this context to help you understand where the product fits, but we do not make any medical claims, and we recommend professional advice whenever you are unsure.",
    "The traditional role of {en} is best understood by looking at how it is grouped in classical practice. It belongs to the {cat} family, where items are usually used together rather than in isolation, and where a household builds experience over time. Traditional practice values moderate, regular use, careful storage and appropriate sourcing. In our catalogue we place it alongside closely related items such as {l1} and {l2} so that customers can compare like with like before ordering.",
]

USAGE = [
    "Practical use in a traditional routine is normally simple: keep the product in its original packaging, store it in a cool dry place away from direct sunlight, and use it consistently as part of your everyday pattern. If the label specifies a quantity or method, follow that. If you are combining this product with others from our {cat} range, do so thoughtfully rather than piling many items together. Traditional practice favours simplicity. Many of our customers organise their shelf by category, which is exactly how our store is arranged, so it is easy to reorder the same product when you run out.",
    "Using {en} as part of a traditional routine is generally straightforward. Because traditional products are often grouped by category, our customers tend to keep this item beside related products such as {l1} and {l2} so that they can reach the right one quickly. Storage is critical: heat, moisture and light degrade traditional herbal products faster than most people expect. Always close the container tightly after use and keep it out of reach of children. Follow the label for any quantity or method; if the label is silent and you are unsure, ask a qualified practitioner.",
    "There is no single traditional way to use {en}, because individual routines vary. What traditional practice does emphasise is consistency and appropriateness. Most households keep a small, organised set of {cat} items rather than a large, random collection, and this product fits naturally into such a set. Store it cool and dry, handle it cleanly, and follow the label for quantity. If you are also using other products from our range, such as {l1} or {l2}, consider how they interact in your routine rather than adding them blindly.",
    "From a practical standpoint, {en} is easiest to use when it is stored sensibly and kept near the items you already rely on. Our customers frequently pair it with {l1} and {l2}, which belong to the same category and are often used in similar situations. Traditional practice favours moderate, regular use over occasional excess, and it relies on the label for any dosage or preparation guidance. Because everyone's needs are different, we recommend consulting a qualified practitioner if you have any doubt about suitability.",
    "Traditional use of {en} is not complicated, but it does benefit from a bit of organisation. Keep it with your other {cat} items, in a cool, dark, dry place, and treat the container carefully so that contents stay fresh. If you are combining products, do so deliberately rather than randomly; our customers often buy {l1} and {l2} together with this item for exactly that reason. Any specific quantity or method should come from the product label or from a qualified practitioner.",
]

QUALITY = [
    "Quality and sourcing matter more in traditional herbal products than most buyers realise. At {store} we select our suppliers carefully and describe products in plain, factual terms so that you know exactly what you are ordering. This {en} is listed as a traditional herbal item, not as a medicine, and we do not make any claim that it diagnoses, treats, cures or prevents any disease. Packaging is designed to protect the contents from moisture and light, and shelf life depends on the specific ingredients and how you store the product.",
    "Every product at {store} is described as it is: a traditional herbal item, offered for general use, with no medical, curative or preventive claims attached. Because the exact ingredients and specifications of a product are determined by the manufacturer, we recommend that you read the packaging that arrives with the product for the authoritative details. Our listing focuses on category, traditional context and usage patterns, which is what most buyers find useful when deciding between similar items in our {cat} range.",
    "We take a conservative approach to describing traditional products. Rather than making health claims we cannot substantiate, we tell you what the product is, where it sits in our catalogue, and how traditional users in Pakistan generally think about it. This {en} is offered as a traditional preparation, and its suitability depends on your personal situation. Nothing on this page should be read as medical advice, and if you are pregnant, nursing, taking medication or managing a health condition, please speak with a qualified professional before use.",
    "Selection at {store} is guided by three principles: honest description, sensible sourcing and clear categorisation. This {en} is listed under {cat} → {sub}, which tells you exactly where it belongs in the traditional Pakistani herbal landscape. We do not embellish, and we do not repeat unverified claims. What we do provide is a clear description, a stable product page, and consistent availability so that you can reorder the same item when you need it.",
    "The way we describe {en} reflects how we describe every product: as a traditional herbal item, honestly and without exaggeration. {store} does not make medical claims, and we encourage customers to treat all traditional products with the same caution they would apply to any new item in their routine. Read the label carefully, store correctly, and if you have a specific concern, ask a qualified practitioner. This page is intended to help you understand the product and its place in our catalogue, not to replace professional advice.",
]

RELATED_PARA = [
    "If you are building a routine around this product, the items below are the ones our customers most often buy together with it: {links}. All of these sit in the same part of our catalogue, so you can compare them side by side and see which suits your situation best.",
    "Related products from our shelves that fit naturally with this one include {links}. They share the same traditional category, which makes comparison straightforward. Many customers order two or three of them at once so that they have a small, coherent set for regular use.",
    "You may also want to look at {links} from the same section of our store. These products belong to the same traditional family and are frequently reviewed together by customers who are deciding between similar items in our {cat} range.",
    "Customers who ordered this product often went on to add {links} to their cart as well. Each of these is a close companion in the traditional routine and is fully described on its own product page, so you can review ingredients, category and traditional context before deciding.",
    "For a broader selection in the same category, see {links}. They are the most directly relevant products from our master catalogue and each has its own page with detailed, factual information written in the same style you are reading here.",
]

FAQ_BLOCK = [
    "<h3>Frequently asked questions</h3>"
    "<p><strong>Is this a medicine?</strong> No. It is a traditional herbal product and is not intended to diagnose, treat, cure or prevent any disease.</p>"
    "<p><strong>How should I store it?</strong> Keep it in a cool, dry place, away from direct sunlight, and close the container tightly after each use.</p>"
    "<p><strong>Can I use it with other products from this store?</strong> Many customers do, but traditional practice favours simplicity. If you are unsure, consult a qualified practitioner.</p>",

    "<h3>Common questions</h3>"
    "<p><strong>Who is this product for?</strong> It is offered as a traditional herbal item for general use by adults. It is not a substitute for medical advice.</p>"
    "<p><strong>What does the label tell me?</strong> The packaging that arrives with the product carries the manufacturer's ingredients, quantity guidance and shelf-life information; please read it carefully.</p>"
    "<p><strong>Can I combine it with similar products?</strong> Yes, but thoughtfully. See the related products above for items that belong to the same traditional category.</p>",

    "<h3>Buyer questions</h3>"
    "<p><strong>Is this product available year-round?</strong> We aim to keep all {cat} items in stock, but availability can vary. If you cannot order, please try again later or contact us.</p>"
    "<p><strong>Is this suitable for children?</strong> Unless the packaging explicitly states otherwise, traditional herbal products of this type are intended for adults.</p>"
    "<p><strong>Where do you ship?</strong> We ship across Pakistan through our standard courier partners.</p>",

    "<h3>Frequently asked</h3>"
    "<p><strong>Is this the same as the version sold in stores?</strong> We stock the version described on this page; the packaging you receive will carry the manufacturer's own details.</p>"
    "<p><strong>How do I reorder later?</strong> The product page URL is stable. Save it or search by product name on our store to reorder the same item.</p>"
    "<p><strong>Can I use multiple items from this category together?</strong> Yes, and our customers often do. See the related product links above for the most common combinations.</p>",
]

SAFETY = [
    "<p><em>Important: this product is a traditional herbal item. It is not a medicine and is not intended to diagnose, treat, cure or prevent any disease. Keep out of the reach of children, store in a cool dry place, and discontinue use if irritation occurs. If you are pregnant, nursing, taking medication or managing a health condition, consult a qualified professional before use.</em></p>",
    "<p><em>Please note: this is a traditional herbal preparation offered for general use. It is not a substitute for professional medical advice and no therapeutic benefit is claimed. Always read the packaging before use and follow the manufacturer's guidance. Store away from heat and moisture, and keep out of reach of children.</em></p>",
    "<p><em>Disclaimer: this product is sold as a traditional herbal item without any medical claims. Do not use it as a replacement for prescribed treatment. Store correctly, follow the label, and consult a qualified practitioner if you are unsure whether it suits you.</em></p>",
]

# ------------------------------------------------------------------
# INTERNAL LINKING
# ------------------------------------------------------------------
STOP = set(
    "roghan sharbat sirka majun khamira itrifal jawarish laboob safoof kushta hab "
    "tukhm gul barg chhaal jar mool boti beej dana seed seeds oil ka ki ke mix special "
    "khushk khalis desi siyah safaid surkh zard khurd kalan bari sabz khatai roomi hindi "
    "kabuli misri kufi chini shahi motadil pak giri araq 5in1 al shifa new sona herbal "
    "khan multan swat baloch qarshi hamdard ajmal ashraf labs marhaba tayyebi herbion "
    "noorani hashmi shama".split()
)

def toks(slug):
    return [t for t in slug.split('-') if t and t not in STOP and not t.isdigit()]

idx_by_tok = defaultdict(list)
for i, p in enumerate(P):
    for t in set(toks(p[0])):
        idx_by_tok[t].append(i)

def related(i, n=4):
    my = toks(P[i][0])
    seen, out = set(), []
    for t in my:
        for j in idx_by_tok.get(t, []):
            if j != i and j not in seen:
                seen.add(j); out.append(j)
    for j in range(len(P)):
        if len(out) >= n:
            break
        if j != i and j not in seen and P[j][4] == P[i][4]:
            seen.add(j); out.append(j)
    j = 0
    while len(out) < 3 and j < len(P):
        if j != i and j not in out:
            out.append(j)
        j += 1
    return out[:n]

def url(j):
    return BASE + P[j][0] + "/"

def lnk(j):
    return '<a href="%s">%s</a>' % (url(j), P[j][1])

# ------------------------------------------------------------------
# WHATSAPP BUTTON
# ------------------------------------------------------------------
def whatsapp_button(i):
    _, en, ur, brand, cat, sub = P[i]
    product_name = f"{en} - {brand}" if brand else en
    sku = "KHS-%04d" % (i + 1)
    price = random_price(i)

    message = (
        f"Assalam-o-Alaikum Khan Herbal Stores!%0A%0A"
        f"I want to place an order for the following product:%0A%0A"
        f"*Product:* {product_name}%0A"
        f"*SKU:* {sku}%0A"
        f"*Price:* PKR {price}%0A"
        f"*Quantity:* 1%0A%0A"
        f"Please confirm availability and share delivery details.%0A%0A"
        f"Shukriya!"
    )
    # Safely encode any characters that need it (keeps %0A newlines working)
    wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={message}"

    return (
        '<div style="text-align:center;margin:24px 0;">'
        f'<a href="{wa_url}" target="_blank" rel="noopener nofollow" '
        'style="display:inline-block;background:#25D366;color:#ffffff;'
        'padding:14px 28px;border-radius:6px;text-decoration:none;'
        'font-weight:bold;font-size:16px;box-shadow:0 2px 6px rgba(0,0,0,0.15);">'
        '&#128241; Order on WhatsApp'
        '</a>'
        f'<div style="font-size:12px;color:#666;margin-top:6px;">'
        f'Chat with us on WhatsApp: {WHATSAPP_DISPLAY}'
        '</div>'
        '</div>'
    )

# ------------------------------------------------------------------
# DESCRIPTION + SEO
# ------------------------------------------------------------------
def form_of(p):
    c = p[4]
    if c == "Oils":
        return "Oil"
    if c == "Syrups":
        return "Syrup"
    if c == "Vinegars":
        return "Vinegar"
    return p[5]

def short_desc(i):
    _, en, ur, brand, cat, sub = P[i]
    b = f" by {brand}" if brand else ""
    return (f"{en}{b} ({ur}) — traditional {sub.lower()} from {STORE}. "
            f"{form_of(P[i])} category · {cat}. Order online or via WhatsApp.")

def long_desc(i):
    _, en, ur, brand, cat, sub = P[i]
    rel = related(i, 4)
    l = [lnk(j) for j in rel]
    b = f" ({brand})" if brand else ""
    intro = INTRO[i % len(INTRO)].format(store=STORE, en=en + b, cat=cat, l1=l[0], l2=l[1])
    about = f"<h3>About {en} in our {cat} collection</h3><p>{CAT_ABOUT[cat].format(store=STORE, sub=sub)}</p>"
    about2 = (
        f"<p><strong>Product name (Urdu):</strong> {ur}</p>"
        f"<p>This specific listing, <strong>{en}{b}</strong>, sits in the <strong>{sub}</strong> "
        f"sub-category. Its form is <strong>{form_of(P[i])}</strong>. The product is offered as a "
        f"traditional herbal item; exact pack size, ingredients, dosage and certification are "
        f"confirmed on the manufacturer's packaging.</p>"
    )
    trad = f"<h3>Traditional context</h3><p>{TRADITIONAL[i % len(TRADITIONAL)].format(en=en, cat=cat, l1=l[0], l2=l[1])}</p>"
    use = f"<h3>Using it in a routine</h3><p>{USAGE[i % len(USAGE)].format(en=en, cat=cat, l1=l[0], l2=l[1])}</p>"
    qual = f"<h3>Quality, sourcing and how we describe products</h3><p>{QUALITY[i % len(QUALITY)].format(en=en, cat=cat, sub=sub, store=STORE)}</p>"
    relp = f"<h3>Related products from {STORE}</h3><p>{RELATED_PARA[i % len(RELATED_PARA)].format(links=', '.join(l[:3]), cat=cat)}</p>"
    wa   = whatsapp_button(i)
    faq  = FAQ_BLOCK[i % len(FAQ_BLOCK)].format(cat=cat)
    safe = SAFETY[i % len(SAFETY)]
    return "".join([
        f"<p>{intro}</p>", about, about2, trad, use, qual, relp,
        wa, faq, safe,
    ])

def seo_title(i):
    _, en, ur, brand, cat, sub = P[i]
    t = f"{en} – {brand}" if brand else en
    t = f"{t} | Buy Online in Pakistan | {STORE}"
    return t if len(t) <= 60 else t[:57].rstrip() + "..."

def meta_desc(i):
    _, en, ur, brand, cat, sub = P[i]
    b = f" by {brand}" if brand else ""
    m = (f"Buy {en}{b} online in Pakistan from {STORE}. Traditional "
         f"{sub.lower()} in our {cat} range. Order via WhatsApp or cart — fast delivery.")
    return m if len(m) <= 160 else m[:157].rstrip() + "..."

# ------------------------------------------------------------------
# CSV ROW BUILDER
# ------------------------------------------------------------------
COLS = [
    "ID", "Type", "SKU", "Name", "Published", "Is featured?", "Visibility in catalog",
    "Short description", "Description", "Tax status", "Tax class", "In stock?",
    "Stock", "Manage stock?", "Low stock amount",
    "Backorders allowed?", "Sold individually?",
    "Weight (kg)", "Allow customer reviews?", "Sale price", "Regular price",
    "Categories", "Tags", "Shipping class", "Images", "Position",
    "Attribute 1 name", "Attribute 1 value(s)", "Attribute 1 visible", "Attribute 1 global",
    "Slug",
    "Meta: rank_math_focus_keyword",
    "Meta: rank_math_title",
    "Meta: rank_math_description",
    "Meta: rank_math_robots",
    "Meta: _khs_all_keywords",
]

def build_row(i):
    _, en, ur, brand, cat, sub = P[i]
    name = f"{en} - {brand}" if brand else en
    primary, others = build_keywords(en, brand, cat)
    focus = ", ".join([primary] + others)
    allkw = "; ".join([primary] + others)
    price = random_price(i)
    stock = random_stock(i)
    return {
        "ID": "", "Type": "simple", "SKU": "KHS-%04d" % (i + 1),
        "Name": name, "Published": 1, "Is featured?": 0,
        "Visibility in catalog": "visible",
        "Short description": short_desc(i),
        "Description": long_desc(i),
        "Tax status": "taxable", "Tax class": "", "In stock?": 1,
        "Stock": stock, "Manage stock?": 1, "Low stock amount": LOW_STOCK_ALERT,
        "Backorders allowed?": 0, "Sold individually?": 0, "Weight (kg)": "",
        "Allow customer reviews?": 1, "Sale price": "", "Regular price": price,
        "Categories": f"{cat} > {sub}",
        "Tags": f"{cat}, {sub}, {form_of(P[i])}, herbal pakistan",
        "Shipping class": "", "Images": "", "Position": i + 1,
        "Attribute 1 name": "Form", "Attribute 1 value(s)": form_of(P[i]),
        "Attribute 1 visible": 1, "Attribute 1 global": 0,
        "Slug": P[i][0],
        "Meta: rank_math_focus_keyword": focus,
        "Meta: rank_math_title": seo_title(i),
        "Meta: rank_math_description": meta_desc(i),
        "Meta: rank_math_robots": "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1",
        "Meta: _khs_all_keywords": allkw,
    }

# ------------------------------------------------------------------
# SLUG FIXER (companion PHP file)
# ------------------------------------------------------------------
def write_slug_fixer():
    lines = ["<?php",
             "/**",
             " * Khan Herbal Stores — one-time slug fixer",
             " * Upload to your WordPress root (next to wp-load.php) and visit:",
             " *   https://darkcyan-turkey-703045.hostingersite.com/khs_slug_fixer.php",
             " * DELETE this file immediately after the run.",
             " */",
             "require_once(__DIR__ . '/wp-load.php');",
             "header('Content-Type: text/plain; charset=utf-8');",
             ""]
    lines.append("$map = [")
    for i, p in enumerate(P):
        sku  = "KHS-%04d" % (i + 1)
        slug = p[0]
        lines.append(f"    '{sku}' => '{slug}',")
    lines.append("];")
    lines.append("")
    lines.append(r"""
$fixed = 0; $missing = 0; $errors = 0;
foreach ($map as $sku => $slug) {
    $pid = wc_get_product_id_by_sku($sku);
    if (!$pid) { echo "MISSING  $sku\n"; $missing++; continue; }
    $target = sanitize_title($slug);
    $current = get_post_field('post_name', $pid);
    if ($current === $target) { echo "OK       $sku ($target)\n"; continue; }
    $r = wp_update_post(['ID' => $pid, 'post_name' => $target], true);
    if (is_wp_error($r)) {
        echo "ERROR    $sku -> " . $r->get_error_message() . "\n";
        $errors++;
    } else {
        echo "FIXED    $sku: $current -> $target\n";
        $fixed++;
    }
}
echo "\n=== DONE ===\n";
echo "Fixed:   $fixed\n";
echo "Missing: $missing\n";
echo "Errors:  $errors\n";
echo "\nNow DELETE this file from your server.\n";
""")
    with open("khs_slug_fixer.php", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ------------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------------
def validate(rows):
    names = [r["Name"] for r in rows]
    skus = [r["SKU"] for r in rows]
    slugs = [r["Slug"] for r in rows]
    assert len(rows) == 325, "row count != 325"
    assert len(set(names)) == 325, "duplicate names"
    assert len(set(skus)) == 325, "duplicate SKUs"
    assert len(set(slugs)) == 325, "duplicate slugs"
    for r in rows:
        assert not re.search(r'[\u0600-\u06FF]', r["Name"]), \
            f"Non-English characters in Name: {r['Name']}"
    allslugs = set(slugs)
    bad = 0
    total_links = 0
    total_wa = 0
    for r in rows:
        for u in re.findall(r'href="([^"]+)"', r["Description"]):
            if u.startswith(BASE):
                total_links += 1
                if u[len(BASE):].rstrip('/') not in allslugs:
                    bad += 1
            if u.startswith("https://wa.me/"):
                total_wa += 1
    assert bad == 0, f"{bad} broken internal links"
    assert total_wa == 325, f"expected 325 WhatsApp buttons, found {total_wa}"
    d = [r["Description"] for r in rows]
    assert len(set(d)) == 325, "duplicate descriptions"
    for r in rows:
        assert int(r["Regular price"]) >= 100, f"price too low: {r['Regular price']}"
        assert int(r["Stock"]) >= 1, f"stock too low: {r['Stock']}"
    return total_links, total_wa

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    rows = [build_row(i) for i in range(len(P))]
    links, wa_count = validate(rows)
    with open("khan_herbal_stores_FINAL.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    write_slug_fixer()

    wc = [len(re.sub('<[^>]+>', '', r["Description"]).split()) for r in rows]
    prices = [int(r["Regular Price"]) if "Regular Price" in r else int(r["Regular price"]) for r in rows]
    stocks = [int(r["Stock"]) for r in rows]
    print("Products processed     :", len(P))
    print("Rows written           :", len(rows))
    print("Internal links         :", links)
    print("WhatsApp buttons       :", wa_count)
    print("Min words per desc     :", min(wc))
    print("Avg words per desc     :", sum(wc) // len(wc))
    print("Unique slugs / SKUs    :", len({r["Slug"] for r in rows}), "/", len({r["SKU"] for r in rows}))
    print("Price range (PKR)      :", min(prices), "-", max(prices))
    print("Stock range            :", min(stocks), "-", max(stocks))
    print("Names in English only  :", all(not re.search(r'[\u0600-\u06FF]', r["Name"]) for r in rows))
    print("WhatsApp number used   :", WHATSAPP_NUMBER)
    print("Files written          : khan_herbal_stores_FINAL.csv, khs_slug_fixer.php")

if __name__ == "__main__":
    main()