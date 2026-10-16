
STAFF_SPECIALTIES = {
    "Mr. Kingsley": ("Network", "Software"),
    "Mr. Godswill": ("Network",),
    "Mr. Ayuba": ("Hardware",),
    "Mr. Gabriel": ("Hardware",),
    "Mr. Emmanuel": ("Software",),
    "Mr. Onche": ("Other",),
}


def recommend_staff(category):
    """Recommend staff members who specialize in a ticket category."""

    if not isinstance(category, str) or category not in (
        "Network", "Hardware", "Software", "Other"
    ):
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )

    recommendations = []

    for staff_member, specialties in STAFF_SPECIALTIES.items():
        if category in specialties:
            recommendations.append(staff_member)

    return recommendations
