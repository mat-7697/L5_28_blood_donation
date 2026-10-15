
"""Blood donation management system demonstration."""

import os
import tempfile
from datetime import date, timedelta

OFFICER_PASSWORD = "bloodbank-demo"

donors = []

stock = {"A+": 0, "A-": 0, "B+": 0, "B-": 0, "O+": 0, "O-": 0, "AB+": 0, "AB-": 0}

COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(stock),
}


def register_donor(
    donor_name,
    blood_group,
    age,
    last_donation=None,
    notes=None,
):
    """Register a donor after checking the age and blood group."""
    assert blood_group in stock, "Unknown blood group"

    if notes is None:
        notes = []

    if age < 18 or age > 65:
        notes.append(
            donor_name + " is not eligible because of age"
        )
        return False

    donors.append(
        {
            "name": donor_name,
            "group": blood_group,
            "last": last_donation,
        }
    )
    return True


def can_donate(donor):
    """Check whether a donor can donate again."""
    if donor["last"] is None:
        return True

    return (
        date.today() - donor["last"]
        >= timedelta(days=90)
    )


def record_donation(donor_name, units=1):
    """Record a donation and update blood stock."""
    for donor in donors:
        if (
            donor["name"] == donor_name
            and can_donate(donor)
        ):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True

    return False


def units_for(patient_group):
    """Calculate available units compatible with a patient."""
    try:
        return sum(
            stock[group]
            for group in COMPATIBLE[patient_group]
        )
    except KeyError:
        return 0


def is_universal(blood_group):
    """Check whether the group is O-negative or AB-positive."""
    return blood_group in {"O-", "AB+"}


def low_stock(threshold=2):
    """Return blood groups with stock below the threshold."""
    return [
        group
        for group, units in stock.items()
        if units < threshold
    ]



def donor_sheet_path():
    """Return a temporary path for a donor sheet."""
    # Security-related change will be handled in the Bandit stage.
    return tempfile.mktemp(suffix=".csv")


def notify_donors(phone_list):
    """Run the existing donor notification helper."""
    # Security-related change will be handled in the Bandit stage.
    os.system("send-sms " + " ".join(phone_list))


def main():
    """Run the blood donation management demonstration."""
    register_donor("Arjun", "O+", 25)
    register_donor(
        "Priya",
        "A+",
        30,
        date.today() - timedelta(days=30),
    )
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)

    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")

    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock()) # below 2 units

    eligible=[donor["name"] for donor in donors if can_donate(donor)]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
