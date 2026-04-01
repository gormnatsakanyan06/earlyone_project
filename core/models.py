from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from smart_selects.db_fields import ChainedForeignKey
import uuid


class QRCode(models.Model):
    text = models.TextField(unique=True)  
    image = models.ImageField(upload_to='media/qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Service(models.Model):
    SERVICE_TYPES = [
        ("water", "Ջրի սպասարկում"),
        ("energy", "Հոսանքի սպասարկում"),
        ("gas", "Գազի սպասարկում")
    ]

    name = models.CharField(max_length=100, null=True, blank=True)
    
    type = models.CharField(max_length=20, choices=SERVICE_TYPES, unique=True)
    image = models.ImageField(upload_to='media/utility/', null=True, blank=True)

    def __str__(self):
        return self.name if self.name else self.get_type_display()


class ServiceBranch(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="branches",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=80, null=True)
    branchCode = models.IntegerField(unique=True, null=True)
    address = models.CharField(max_length=80, unique=True)
    phone = models.CharField(max_length=80, unique=True, null=True)

    def __str__(self):
        return f"{self.address}"


class ServiceAction(models.Model):
    ACTION_TYPES = [
        ("Jrachapi poxarinum", "Ջրաչափի փոխարինում, տեղադրում"),
        ("Avartakan akti hastatum", "Ավարտական ակտի հաստատում"),
        ("Hashvichi poxarinum", "Հաշվիչի փոխարինում / տեղակայում"),
        ("Hzorutyan poxarinum", "Հզորության փոխարինում"),
        ("Gazi sarqi poxarinum", "Գազի սարքի փոխարինում, տեղադրում"),
    ]

    actiontype = models.CharField(max_length=100, choices=ACTION_TYPES, null=True)

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="actions"
    )

    branch = ChainedForeignKey(
        ServiceBranch,
        chained_field="service",
        chained_model_field="service",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
        null=True
    )

    scheduled_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        service_display = str(self.service)
        branch_display = self.branch.address if self.branch else "No Branch"
        action_display = self.get_actiontype_display()
        
        return f"{service_display} | {branch_display} | {action_display}"


class Telecom(models.Model):
    TELECOM_TYPES = [
        ("viva", "Վիվասել"),
        ("team", "Թիմ"),
        ("ucom", "Յուքոմ")
    ]
    telecom = models.CharField(max_length=30, choices=TELECOM_TYPES, unique=True)
    image = models.ImageField(upload_to='media/telecom/', null=True, blank=True)



    def __str__(self):
        return self.get_telecom_display()


class TelecomBranch(models.Model):
    telecom = models.ForeignKey(
        Telecom,
        on_delete=models.CASCADE,
        related_name="branches",
        null=True,
        blank=True
    )
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=80, unique=True)
    branchCode = models.CharField(max_length=80, unique=True, null=True)
    phone = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f"{self.address}"


class TelecomAction(models.Model):
    ACTION_TYPES = [
        ("bajanord", "Դառնալ բաժանորդ"),
        ("vcharum", "Վճարումներ"),
        ("aqsesuar", "Հեռախոսների, աքսեսուարների և սարքավորումների ձեռքբերում"),
        ("xorhrdatvutyun", "Խորհրդատվություն և աջակցում")
    ]
    telecomaction = models.CharField(max_length=30, choices=ACTION_TYPES, null=True)

    telecom = models.ForeignKey(
        Telecom,
        on_delete=models.CASCADE,
        related_name="actions"
    )

    branch = ChainedForeignKey(
        TelecomBranch,
        chained_field="telecom",
        chained_model_field="telecom",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
        null=True
    )

    scheduled_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.telecom.get_telecom_display()} | {self.branch.address} | {self.get_telecomaction_display()}"



class Government(models.Model):
    GOVERNMENT_TYPES = [
        ("ngn", "Հաշվառման-քննական ստորաբաժանումներ(ՆԳՆ)"),
        ("arxiv", "Հայաստանի ազգային արխիվ"),
        ("kadastr", "Կադաստրի կոմիտե")
    ]

    government = models.CharField(max_length=20, choices=GOVERNMENT_TYPES, unique=True)
    image = models.ImageField(upload_to='media/government/', null=True, blank=True)



    def __str__(self):
        return self.get_government_display()


class GovernmentBranch(models.Model):
    government = models.ForeignKey(
        Government,
        on_delete=models.CASCADE,
        related_name="branches",
    )
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=80, unique=True)
    branchCode = models.CharField(max_length=80, unique=True, null=True)
    phone = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f"{self.address}"


class GovernmentAction(models.Model):
    ACTION_TYPES = [
        ("tesakan", "Վարորդական վկայական ստանալու տեսական քննություն"),
        ("gorcnakan", "Վարորդական վկայական ստանալու գործնական քննություն"),
        ("dimumH", "Դիմումի հանձնում"),
        ("dimumS", "Դիմումի ստացում"),
        ("pastatuxt", "Ստանալ փաստաթուղթ")
    ]

    governmentaction = models.CharField(max_length=30, choices=ACTION_TYPES, unique=True, null=True)

    government = models.ForeignKey(
        Government,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    branch = ChainedForeignKey(
        GovernmentBranch,
        chained_field="government",
        chained_model_field="government",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f"{self.government.get_government_display()} | {self.branch.address} | {self.get_governmentaction_display()}"

    scheduled_time = models.DateTimeField(null=True, blank=True)


class Bank(models.Model):
    BANK_TYPES = [
        ("ameria", "Ամերիա բանկ"),
        ("evoca", "Էվոկա բանկ"),
        ("ineco", "Ինեկո բանկ"),
        ("akba", "Ակբա բանկ")
    ]

    bank = models.CharField(max_length=20, choices=BANK_TYPES, unique=True)
    image = models.ImageField(upload_to='media/bank/', null=True, blank=True)


    def __str__(self):
        return self.get_bank_display()


class BankBranch(models.Model):
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="branches",
        null=True,
        blank=True
    )
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=80, unique=True)
    branchCode = models.CharField(max_length=80, unique=True, null=True)
    phone = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f"{self.address}"


class BankAction(models.Model):
    ACTION_TYPES = [
        ("qart", "Քարտերի սպասարկում"),
        ("vark", "Վարկ / վարկային գիծ"),
        ("avand", "Ավանդներ"),
        ("kanxik", "Կանխիկ գործարքներ")
    ]
    bankaction = models.CharField(max_length=30, choices=ACTION_TYPES, null=True)

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="actions"
    )

    branch = ChainedForeignKey(
        BankBranch,
        chained_field="bank",
        chained_model_field="bank",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
        null=True
    )

    scheduled_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.bank.get_bank_display()} | {self.branch.address} | {self.get_bankaction_display()}"


class Contact(models.Model):
    types= [("Customer", "Հաճախորդ"),
           ("Partner", "Գործընկեր"),
           ]
    type = models.CharField(max_length=20, choices=types)
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    phone = models.CharField(max_length=80, unique=True, null=True)
    message = models.CharField(max_length=222)
    company = models.CharField(max_length=80,null=True)

    def __str__(self):
        return f"{self.get_type_display()} | {self.type} | {self.name} | {self.email} | {self.phone}"
    


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('finance', 'Ֆինանսներ'),
        ('government', 'Պետական'),
        ('telecom', 'Տելեկոմ'),
        ('utility', 'Կոմունալ'),
    ]

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    #Hetaga anter nkarner

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    service_action = GenericForeignKey('content_type', 'object_id')

    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(null=True, blank=True)

    #qri masna
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_code = models.OneToOneField("QRCode", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.category}"




class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    svg_path = models.TextField(help_text="Paste the 'd' attribute string here")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='providers')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    images = models.ImageField(upload_to='media/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name