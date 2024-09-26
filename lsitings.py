import requests
from users import user_ava, user_jan

my_listings = {
    "listings": [

        {
            "id": "1lnnygENuh8Lmv4sXzbTK",
            "image_url": "https://images.airtasker.com/v7/https://listings-attachments.s3.ap-southeast-2.amazonaws.com/bdafdf8f-8e7f-4a75-b1fb-6435a7ad50ae.jpg",
            "title": "Professional ATS compliant Cover Letter",
            "label": "PUBLISHED",
            "label_color": "#20BF6F",
            "label_tooltip": "Your listing was successfully published! It is now live and ready to be booked by customers.",
            "buttons": [
                {
                    "icon": "icon_player_pause",
                    "label": "Pause",
                    "disabled": False,
                    "button_action": "pause",
                    "action": {
                        "type": "pause"
                    }
                },
                {
                    "icon": "icon_library_edit",
                    "label": "Edit",
                    "disabled": False,
                    "button_action": "edit",
                    "action": {
                        "type": "edit",
                        "url": "https://www.airtasker.com/listings/professional-ats-compliant-cover-letter-57552/1lnnygENuh8Lmv4sXzbTK/edit"
                    }
                },
                {
                    "icon": "icon_library_bin",
                    "label": "Delete",
                    "disabled": False,
                    "button_action": "delete",
                    "action": {
                        "type": "delete"
                    }
                }
            ],
            "action": {
                "type": "deep_link",
                "on_click_deep_link": "https://www.airtasker.com/listings/professional-ats-compliant-cover-letter-57552/1lnnygENuh8Lmv4sXzbTK?initiated_from=My%20Listings&initiatedFrom=My%20Listings"
            }
        },
        {
            "id": "6qfpQsiNykVbdPS8wWUbTb",
            "image_url": "https://images.airtasker.com/v7/https://listings-attachments.s3.ap-southeast-2.amazonaws.com/571d886c-e619-4db5-bfdd-e90b53fb427b.jpg",
            "title": "Administration Resume",
            "label": "PUBLISHED",
            "label_color": "#20BF6F",
            "label_tooltip": "Your listing was successfully published! It is now live and ready to be booked by customers.",
            "buttons": [
                {
                    "icon": "icon_player_pause",
                    "label": "Pause",
                    "disabled": False,
                    "button_action": "pause",
                    "action": {
                        "type": "pause"
                    }
                },
                {
                    "icon": "icon_library_edit",
                    "label": "Edit",
                    "disabled": False,
                    "button_action": "edit",
                    "action": {
                        "type": "edit",
                        "url": "https://www.airtasker.com/listings/administration-resume-65475/6qfpQsiNykVbdPS8wWUbTb/edit"
                    }
                },
                {
                    "icon": "icon_library_bin",
                    "label": "Delete",
                    "disabled": False,
                    "button_action": "delete",
                    "action": {
                        "type": "delete"
                    }
                }
            ],
            "action": {
                "type": "deep_link",
                "on_click_deep_link": "https://www.airtasker.com/listings/administration-resume-65475/6qfpQsiNykVbdPS8wWUbTb?initiated_from=My%20Listings&initiatedFrom=My%20Listings"
            }
        },
        {
            "id": "6SS3dlpNsH3nmL7UO0JzdN",
            "image_url": "https://images.airtasker.com/v7/https://listings-attachments.s3.ap-southeast-2.amazonaws.com/9f53e3e7-1a4d-4fd9-89e5-991e3fd9f41a.jpg",
            "title": "Professional ATS compliant Cover Letter",
            "label": "PUBLISHED",
            "label_color": "#20BF6F",
            "label_tooltip": "Your listing was successfully published! It is now live and ready to be booked by customers.",
            "buttons": [
                {
                    "icon": "icon_player_pause",
                    "label": "Pause",
                    "disabled": False,
                    "button_action": "pause",
                    "action": {
                        "type": "pause"
                    }
                },
                {
                    "icon": "icon_library_edit",
                    "label": "Edit",
                    "disabled": False,
                    "button_action": "edit",
                    "action": {
                        "type": "edit",
                        "url": "https://www.airtasker.com/listings/professional-ats-compliant-cover-letter-76851/6SS3dlpNsH3nmL7UO0JzdN/edit"
                    }
                },
                {
                    "icon": "icon_library_bin",
                    "label": "Delete",
                    "disabled": False,
                    "button_action": "delete",
                    "action": {
                        "type": "delete"
                    }
                }
            ],
            "action": {
                "type": "deep_link",
                "on_click_deep_link": "https://www.airtasker.com/listings/professional-ats-compliant-cover-letter-76851/6SS3dlpNsH3nmL7UO0JzdN?initiated_from=My%20Listings&initiatedFrom=My%20Listings"
            }
        },
        {
            "id": "hE52omyL27QqHnNJSJf1I",
            "image_url": "https://images.airtasker.com/v7/https://listings-attachments.s3.ap-southeast-2.amazonaws.com/9f53e3e7-1a4d-4fd9-89e5-991e3fd9f41a.jpg",
            "title": "Professional ATS compliant Cover Letter",
            "label": "PUBLISHED",
            "label_color": "#20BF6F",
            "label_tooltip": "Your listing was successfully published! It is now live and ready to be booked by customers.",
            "buttons": [
                {
                    "icon": "icon_player_pause",
                    "label": "Pause",
                    "disabled": False,
                    "button_action": "pause",
                    "action": {
                        "type": "pause"
                    }
                },
                {
                    "icon": "icon_library_edit",
                    "label": "Edit",
                    "disabled": False,
                    "button_action": "edit",
                    "action": {
                        "type": "edit",
                        "url": "https://www.airtasker.com/listings/professional-ats-compliant-cover-letter-86775/hE52omyL27QqHnNJSJf1I/edit"
                    }
                },
                {
                    "icon": "icon_library_bin",
                    "label": "Delete",
                    "disabled": False,
                    "button_action": "delete",
                    "action": {
                        "type": "delete"
                    }
                }
            ],
            "action": {
                "type": "deep_link",
                "on_click_deep_link": "https://www.airtasker.com/listings/professional-ats-compliant-cover-letter-86775/hE52omyL27QqHnNJSJf1I?initiated_from=My%20Listings&initiatedFrom=My%20Listings"
            }
        },
        {
            "id": "4kxuni1v92Aa1l0e4UG46a",
            "image_url": "https://images.airtasker.com/v7/https://listings-attachments.s3.ap-southeast-2.amazonaws.com/8fccf9f4-a089-41d1-b916-3a77681314ab.jpg",
            "title": "Tailored Resume ",
            "label": "PUBLISHED",
            "label_color": "#20BF6F",
            "label_tooltip": "Your listing was successfully published! It is now live and ready to be booked by customers.",
            "buttons": [
                {
                    "icon": "icon_player_pause",
                    "label": "Pause",
                    "disabled": False,
                    "button_action": "pause",
                    "action": {
                        "type": "pause"
                    }
                },
                {
                    "icon": "icon_library_edit",
                    "label": "Edit",
                    "disabled": False,
                    "button_action": "edit",
                    "action": {
                        "type": "edit",
                        "url": "https://www.airtasker.com/listings/tailored-resume-74850/4kxuni1v92Aa1l0e4UG46a/edit"
                    }
                },
                {
                    "icon": "icon_library_bin",
                    "label": "Delete",
                    "disabled": False,
                    "button_action": "delete",
                    "action": {
                        "type": "delete"
                    }
                }
            ],
            "action": {
                "type": "deep_link",
                "on_click_deep_link": "https://www.airtasker.com/listings/tailored-resume-74850/4kxuni1v92Aa1l0e4UG46a?initiated_from=My%20Listings&initiatedFrom=My%20Listings"
            }
        },
        {
            "id": "7C7QtmHtJAKNOvw3jLcMGj",
            "image_url": "https://images.airtasker.com/v7/https://listings-attachments.s3.ap-southeast-2.amazonaws.com/724381db-b865-43b6-a74a-1c278c025362.jpg",
            "title": "Scrap information from website",
            "label": "PUBLISHED",
            "label_color": "#20BF6F",
            "label_tooltip": "Your listing was successfully published! It is now live and ready to be booked by customers.",
            "buttons": [
                {
                    "icon": "icon_player_pause",
                    "label": "Pause",
                    "disabled": False,
                    "button_action": "pause",
                    "action": {
                        "type": "pause"
                    }
                },
                {
                    "icon": "icon_library_edit",
                    "label": "Edit",
                    "disabled": False,
                    "button_action": "edit",
                    "action": {
                        "type": "edit",
                        "url": "https://www.airtasker.com/listings/scrap-information-from-website-15160/7C7QtmHtJAKNOvw3jLcMGj/edit"
                    }
                },
                {
                    "icon": "icon_library_bin",
                    "label": "Delete",
                    "disabled": False,
                    "button_action": "delete",
                    "action": {
                        "type": "delete"
                    }
                }
            ],
            "action": {
                "type": "deep_link",
                "on_click_deep_link": "https://www.airtasker.com/listings/scrap-information-from-website-15160/7C7QtmHtJAKNOvw3jLcMGj?initiated_from=My%20Listings&initiatedFrom=My%20Listings"
            }
        }
    ],
    "response_rate_box": {
        "description": "Responded to 3/3 new enquiries within 24hrs",
        "response_rate_percentage": 100
    },
    "booking_requests_box": {
        "type": "empty-booking-requests"
    },
    "meta": {
        "next_page_token": ""
    }
}
