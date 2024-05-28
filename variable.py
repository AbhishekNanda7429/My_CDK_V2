# # from datetime import datetime, timedelta

# # # Set start time to 1 hour back from now and end time to now
# # start_datetime = datetime.now() - timedelta(hours=1)
# # end_datetime = datetime.now()

# # Global Variables
# NOS_ESP_SECRET = "marketosecret"
# OT_SECRET = "one_trust_secret"
# KCC_ESP_SECRET = "eloquasecret"
# CLE_ESP_SECRET = "eloquasecret"#added this variable
# NOS_ESP_ENDPOINT = "https://281-PON-571.mktorest.com/identity/oauth/token"
# KCC_ESP_ENDPOINT = "https://login.eloqua.com/auth/oauth2/token"
# CLE_ESP_ENDPOINT = "https://login.eloqua.com/auth/oauth2/token" #added thiss variable
# #OT_ENDPOINT = "https://uat.onetrust.com/api/access/v1/oauth/token"
# OT_AUTH_URL = "https://uat.onetrust.com"
# OT_CONSENT_URL = "https://nfl-uat-privacy.my.onetrust.com"

# NOS_OAUTH_TYPE = "credentials"
# KCC_OAUTH_TYPE = "refresh_token"
# CLE_OAUTH_TYPE = "refresh_token"

# NOS_BASE_URL_UNSUBSCRIBE_LINK = ""
# KCC_BASE_URL_UNSUBSCRIBE_LINK = ""
# CLE_BASE_URL_UNSUBSCRIBE_LINK = ""

# BATCH_SIZE = "300"
# BUCKET_NAME = "nfl-dna-onetrust-audit-bkt-dev"


# # NOS Club Variables
# NOS_FIELDS_LIST = '["firstName", "lastName","email"]'
# NOS_OT_PURPOSES = {
#     "NOS-YOUTH": "7dec8a2c-ca99-42c4-b0e6-bc8ffa30b45c",
#     "NOS-STW": "a45afa94-312c-4499-99dd-90a403c34954",
#     "NOS-INJ": "4926150f-cfe8-42c3-a620-67b2f6175259",
#     "NOS-SGP": "c41ba9f3-ba1b-4128-9f77-c718a1e9872a",
#     "NOS-TICKETING": "92d2dfc2-c1e1-40c1-badd-8f03fe10a6a1",
#     "NOS-NEWS": "f88c10f9-4cb9-4e32-b78f-8e9fd095211a",
#     "NOS-OFFERS": "5a224076-e5d9-4a88-8ab5-27bb9e942b37",
#     "NOS-PRIVACYPOLICY": "80d84c10-0725-4f18-bd06-868420c3e666",
#     "NOS-TERMSOFSERVICE": "f68dba19-4921-42ec-8a53-94aa7a9fe478",
#     "NOS-ACCDELETION": "65af4582-2663-427a-858e-bdcff4bbde6f" }

# # KCC Club Variables 
# KCC_BASE_URL_UNSUBSCRIBE_LINK = ""
# KCC_CONTACT_VIEW_ID = "100239"
# KCC_ELOQUA_EXPORT_URL="https://secure.p01.eloqua.com/API/REST/2.0/data/contact/view"
# KCC_ELOQUA_IMPORT_URL="https://secure.p01.eloqua.com/api/bulk/2.0"
# KCC_EXPORT_BATCH_SIZE="100"
# KCC_IMPORT_BATCH_SIZE="100"
# KCC_OT_PURPOSES = {
#     "KCC-AE": "8ea25cb1-1058-4f58-b94a-1460ebac6b10",
#     "KCC-PARTNER": "bc0b0331-7145-4ace-9266-e90f3e48f962",
#     "KCC-NEWS": "fb7c4b14-56b3-41a4-9049-fd3d5fcfd883",
#     "KCC-OFFERS": "b7106168-4018-4dba-ad58-c57d1c9b829a",
#     "KCC-PRIVACYPOLICY": "ef2f1d00-48c8-433a-9955-f3cd45b1159f",
#     "KCC-TERMSOFSERVICE": "c8ffae28-05db-47a7-a1e7-0246b7790e13",
#     "KCC-ACCDELETION": "60e8c5c8-3391-4063-b428-b2269ccbaf5e"
# }


# # CLE Club Variables

# CLE_BASE_URL_UNSUBSCRIBE_LINK = ""
# CLE_CONTACT_VIEW_ID = "100239"
# CLE_ELOQUA_EXPORT_URL="https://secure.p01.eloqua.com/API/REST/2.0/data/contact/view"
# CLE_ELOQUA_IMPORT_URL="https://secure.p01.eloqua.com/api/bulk/2.0"
# CLE_EXPORT_BATCH_SIZE="100"
# CLE_IMPORT_BATCH_SIZE="100"
# CLE_OT_PURPOSES = {
#     "CLE-CBSE": "b9a6ee0c-3603-4812-9fab-d6f136d8e287",
#     "CLE-HSG": "dca73890-a1a2-4220-9d78-c0b4a496db51",
#     "CLE-TICKETING": "95088612-1b1c-4ca8-a2a7-655a9740850f",
#     "CLE-YOUTH": "e087f17f-3c4b-49c7-ac23-38e67471450d",
#     "CLE-NEWS": "038661bf-0f00-4287-94a9-25128c34a217",
#     "CLE-OFFERS": "8b7302d9-6bce-4acf-9d76-3a531974d35b",
#     "CLE-PRIVACYPOLICY": "e37ddd0d-92cb-41da-8e80-830cdecc58b5",
#     "CLE-TERMSOFSERVICE": "041af935-8354-4929-9e99-2aa8e7c1c375",
#     "CLE-ACCDELETION": "d6e83e10-1e41-4481-a89f-990b8a4f24cc"
# }

#------------------------------------------------------------------
#Global variable
OT_SECRET = "one_trust_secret"
OT_AUTH_URL = "https://uat.onetrust.com"
OT_CONSENT_URL = "https://nfl-uat-privacy.my.onetrust.com"
BATCH_SIZE = "300"
BUCKET_NAME = "nfl-dna-onetrust-audit-bkt-dev"
POWERTOOLS_LOG_LEVEL = "DEBUG"

#NOS Variable
NOS_ESP_SECRET = "marketosecret"
NOS_ESP_ENDPOINT = "https://281-PON-571.mktorest.com/identity/oauth/token"
NOS_OAUTH_TYPE = "credentials"
NOS_FIELDS_LIST = '["firstName", "lastName","email"]'
NOS_BASE_URL_UNSUBSCRIBE_LINK = ""
NOS_OT_PURPOSES = {
    "NOS-YOUTH": "7dec8a2c-ca99-42c4-b0e6-bc8ffa30b45c",
    "NOS-STW": "a45afa94-312c-4499-99dd-90a403c34954",
    "NOS-INJ": "4926150f-cfe8-42c3-a620-67b2f6175259",
    "NOS-SGP": "c41ba9f3-ba1b-4128-9f77-c718a1e9872a",
    "NOS-TICKETING": "92d2dfc2-c1e1-40c1-badd-8f03fe10a6a1",
    "NOS-NEWS": "f88c10f9-4cb9-4e32-b78f-8e9fd095211a",
    "NOS-OFFERS": "5a224076-e5d9-4a88-8ab5-27bb9e942b37",
    "NOS-PRIVACYPOLICY": "80d84c10-0725-4f18-bd06-868420c3e666",
    "NOS-TERMSOFSERVICE": "f68dba19-4921-42ec-8a53-94aa7a9fe478",
    "NOS-ACCDELETION": "65af4582-2663-427a-858e-bdcff4bbde6f" 
    }

#KCC Variable
KCC_ESP_SECRET = "eloquasecret"
KCC_ESP_ENDPOINT = "https://login.eloqua.com/auth/oauth2/token"
KCC_OAUTH_TYPE = "refresh_token"
KCC_BASE_URL_UNSUBSCRIBE_LINK = ""
KCC_CONTACT_VIEW_ID = "100239"
KCC_ELOQUA_EXPORT_URL="https://secure.p01.eloqua.com/API/REST/2.0/data/contact/view"
KCC_ELOQUA_IMPORT_URL="https://secure.p01.eloqua.com/api/bulk/2.0"
KCC_EXPORT_BATCH_SIZE="100"
KCC_IMPORT_BATCH_SIZE="100"
KCC_OT_PURPOSES = {
    "KCC-AE": "8ea25cb1-1058-4f58-b94a-1460ebac6b10",
    "KCC-PARTNER": "bc0b0331-7145-4ace-9266-e90f3e48f962",
    "KCC-NEWS": "fb7c4b14-56b3-41a4-9049-fd3d5fcfd883",
    "KCC-OFFERS": "b7106168-4018-4dba-ad58-c57d1c9b829a",
    "KCC-PRIVACYPOLICY": "ef2f1d00-48c8-433a-9955-f3cd45b1159f",
    "KCC-TERMSOFSERVICE": "c8ffae28-05db-47a7-a1e7-0246b7790e13",
    "KCC-ACCDELETION": "60e8c5c8-3391-4063-b428-b2269ccbaf5e"
}

#CLE Variable
CLE_ESP_SECRET = "eloquasecret"
CLE_ESP_ENDPOINT = "https://login.eloqua.com/auth/oauth2/token"
CLE_OAUTH_TYPE = "refresh_token"
CLE_BASE_URL_UNSUBSCRIBE_LINK = ""
CLE_CONTACT_VIEW_ID = "100239"
CLE_ELOQUA_EXPORT_URL="https://secure.p01.eloqua.com/API/REST/2.0/data/contact/view"
CLE_ELOQUA_IMPORT_URL="https://secure.p01.eloqua.com/api/bulk/2.0"
CLE_EXPORT_BATCH_SIZE="100"
CLE_IMPORT_BATCH_SIZE="100"
CLE_OT_PURPOSES = {
    "CLE-CBSE": "b9a6ee0c-3603-4812-9fab-d6f136d8e287",
    "CLE-HSG": "dca73890-a1a2-4220-9d78-c0b4a496db51",
    "CLE-TICKETING": "95088612-1b1c-4ca8-a2a7-655a9740850f",
    "CLE-YOUTH": "e087f17f-3c4b-49c7-ac23-38e67471450d",
    "CLE-NEWS": "038661bf-0f00-4287-94a9-25128c34a217",
    "CLE-OFFERS": "8b7302d9-6bce-4acf-9d76-3a531974d35b",
    "CLE-PRIVACYPOLICY": "e37ddd0d-92cb-41da-8e80-830cdecc58b5",
    "CLE-TERMSOFSERVICE": "041af935-8354-4929-9e99-2aa8e7c1c375",
    "CLE-ACCDELETION": "d6e83e10-1e41-4481-a89f-990b8a4f24cc"
}
