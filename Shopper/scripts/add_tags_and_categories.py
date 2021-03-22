from Recipes.models import Tag, Category

categories = ['Płatki', 'Musli', 'Dżemy, miody, kremy', 'Konserwy i dania gotowe', 'Przetwory warzywne i owocowe',
              'Sosy, oleje, ocet', 'Sypkie i produkty zbożowe', 'Przyprawy i dodatki kulinarne', 'Słodycze',
              'Bakalie', 'Mięso', 'Mrożonki', 'Ryby']

tags = ['Obiad', 'Kolacja', 'Wypieki', 'Śniadanie', 'Wege', 'Mięso', 'Ryby', 'Strączki']


def run():
    for c in categories:
        Category.objects.get_or_create(category=c)
    for t in tags:
        Tag.objects.get_or_create(tag=t)
