from django import forms
from django.forms.widgets import TextInput
from datetime import date
from django.core.exceptions import ValidationError
from .models import (
    Accommodation,
    TripOffer,
    AccommodationBooking,
    TripBooking,
    Destination,
    TripTransport,
)


HR_DATE_INPUT_FORMATS = ['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y']


class HRDateInput(TextInput):
    input_type = 'text'
    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('attrs', {}) or {}
        attrs.setdefault('placeholder', 'dd.mm.gggg.')
        attrs.setdefault('inputmode', 'numeric')
        attrs.setdefault('pattern', r'^\d{2}\.\d{2}\.\d{4}$')
        attrs.setdefault('class', 'w-full border rounded-lg p-2')
        super().__init__(attrs=attrs, *args, **kwargs)


class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['naziv', 'destinacija', 'tip', 'kapacitet_jedinica', 'cijena_po_nocenju', 'zvjezdice']


class TripOfferForm(forms.ModelForm):
    class Meta:
        model = TripOffer
        fields = ['destinacija', 'datum_polaska', 'cijena_osnovno', 'broj_mjesta']
        widgets = {
            'datum_polaska': HRDateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datum_polaska'].input_formats = HR_DATE_INPUT_FORMATS

class AccommodationBookingForm(forms.ModelForm):
    grad = forms.ModelChoiceField(
        queryset=Destination.objects.all(),
        required=False,
        label="Grad / destinacija",
        widget=forms.Select(attrs={'class': 'w-full border rounded-lg p-2', 'id': 'id_grad'})
    )

    class Meta:
        model = AccommodationBooking
        fields = ['grad', 'smjestaj', 'check_in', 'check_out', 'broj_osoba']
        widgets = {
            'check_in': HRDateInput(),
            'check_out': HRDateInput(),
            'smjestaj': forms.Select(attrs={'class': 'w-full border rounded-lg p-2', 'id': 'id_smjestaj'}),
            'broj_osoba': forms.NumberInput(attrs={'class': 'w-full border rounded-lg p-2', 'min': 1, 'id': 'id_broj_osoba'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.fields['smjestaj'].queryset = Accommodation.objects.none()
        else:
            self.fields['smjestaj'].queryset = Accommodation.objects.all()
        self.fields['check_in'].input_formats = HR_DATE_INPUT_FORMATS
        self.fields['check_out'].input_formats = HR_DATE_INPUT_FORMATS
        self.fields['smjestaj'].label_from_instance = lambda obj: f"{obj.naziv} ({obj.destinacija}) - {obj.cijena_po_nocenju} €/noć"

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        smjestaj = cleaned_data.get("smjestaj")
        broj_osoba = cleaned_data.get("broj_osoba")

        if check_in and check_in < date.today():
            self.add_error(None, "Datum prijave ne može biti u prošlosti.")
        if check_in and check_out and check_out <= check_in:
            self.add_error(None, "Datum odjave mora biti nakon datuma prijave.")
        if smjestaj and broj_osoba and broj_osoba > smjestaj.kapacitet_jedinica:
            self.add_error(None, "Previše osoba je odabrano za ovaj smještaj.")

        return cleaned_data


class AccommodationBookingUpdateForm(forms.ModelForm):
    class Meta:
        model = AccommodationBooking
        fields = ['check_in', 'check_out', 'broj_osoba']
        widgets = {
            'check_in': HRDateInput(),
            'check_out': HRDateInput(),
            'broj_osoba': forms.NumberInput(attrs={'class': 'w-full border rounded-lg p-2', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in'].input_formats = HR_DATE_INPUT_FORMATS
        self.fields['check_out'].input_formats = HR_DATE_INPUT_FORMATS

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        broj_osoba = cleaned_data.get("broj_osoba")
        smjestaj = self.instance.smjestaj

        if check_in and check_in < date.today():
            self.add_error(None, "Datum prijave ne može biti u prošlosti.")
        if check_in and check_out and check_out <= check_in:
            self.add_error(None, "Datum odjave mora biti nakon datuma prijave.")
        if smjestaj and broj_osoba and broj_osoba > smjestaj.kapacitet_jedinica:
            self.add_error(None, "Previše osoba je odabrano za ovaj smještaj.")

        return cleaned_data


class TripBookingForm(forms.ModelForm):
    ponuda = forms.ModelChoiceField(
        queryset=TripOffer.objects.all(),
        label="Ponuda",
        widget=forms.Select(attrs={'class': 'w-full border rounded-lg p-2'})
    )
    prijevoz = forms.ModelChoiceField(
        queryset=TripTransport.objects.all(),
        label="Način prijevoza",
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = TripBooking
        fields = ['ponuda', 'prijevoz', 'broj_osoba']
        widgets = {
            'broj_osoba': forms.NumberInput(attrs={'class': 'w-full border rounded-lg p-2', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'ponuda' in self.data:
            try:
                ponuda_id = int(self.data.get('ponuda'))
                self.fields['prijevoz'].queryset = TripTransport.objects.filter(ponuda_id=ponuda_id)
            except (ValueError, TypeError):
                self.fields['prijevoz'].queryset = TripTransport.objects.none()
        elif self.instance.pk:
            self.fields['prijevoz'].queryset = TripTransport.objects.filter(ponuda=self.instance.ponuda)
        else:
            self.fields['prijevoz'].queryset = TripTransport.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        ponuda = cleaned_data.get("ponuda")
        prijevoz = cleaned_data.get("prijevoz")
        broj_osoba = cleaned_data.get("broj_osoba")

        if ponuda and ponuda.datum_polaska < date.today():
            raise ValidationError("Ne možete rezervirati putovanje koje je već prošlo.")

        if prijevoz and broj_osoba and broj_osoba > prijevoz.max_osoba:
            raise ValidationError("Previše osoba je odabrano za ovo vozilo.")

        return cleaned_data


class TripBookingUpdateForm(forms.ModelForm):
    prijevoz = forms.ModelChoiceField(
        queryset=TripTransport.objects.none(),
        widget=forms.RadioSelect,
        required=True,
        label="Način prijevoza"
    )

    class Meta:
        model = TripBooking
        fields = ['prijevoz', 'broj_osoba']
        widgets = {
            'broj_osoba': forms.NumberInput(attrs={'class': 'w-full border rounded-lg p-2', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.ponuda:
            self.fields['prijevoz'].queryset = TripTransport.objects.filter(ponuda=self.instance.ponuda)

    def clean(self):
        cleaned_data = super().clean()
        prijevoz = cleaned_data.get("prijevoz")
        broj_osoba = cleaned_data.get("broj_osoba")
        ponuda = self.instance.ponuda

        if ponuda and ponuda.datum_polaska < date.today():
            self.add_error(None, "Ne možete izmijeniti putovanje koje je već prošlo.")
        if prijevoz and broj_osoba and broj_osoba > prijevoz.max_osoba:
            self.add_error(None, "Previše osoba je odabrano za ovo vozilo.")

        return cleaned_data
