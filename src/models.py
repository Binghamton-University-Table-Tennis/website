from django.db import models
from django.utils import timezone

# Create your models here.
class Greeting(models.Model):
    Count = models.IntegerField(editable=False, default = 0)

    def get_absolute_url(self):
        return "/summary"

    class Meta:
        db_table = "visits"
        verbose_name_plural = "Visits"

    def __unicode__(self):
       return "Front page visits: " + str(self.Count)

class Players(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Rating = models.IntegerField(editable=False, default=1000)
    Matches_Won = models.IntegerField(editable=False, default=0)
    Matches_Lost = models.IntegerField(editable=False, default=0)
    Matches_Played = models.IntegerField(editable=False, default=0)
    Win_Rate =models.IntegerField(editable=False, default=0)
    Standing = models.IntegerField(choices=[(1, "Freshman"), (2, "Sophomore"), (3, "Junior"), (4, "Senior"), (5, "Grad"), (6, "Unknown")])
    Played_This_Week = models.IntegerField(editable=False, default=0)
    Attendance = models.IntegerField(editable=False, default=0)
    Lateness = models.IntegerField(editable=False, default=0)
    LastSeen = models.DateField(editable=False, default=timezone.now)
    Email = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return "/attendance"

    class Meta:
        db_table = "players"
        verbose_name_plural = "Players"

    def __unicode__(self):
       return (self.First_Name + " " + self.Last_Name)

class Matches(models.Model):
    Winner_First_Name = models.CharField(max_length=20)
    Winner_Last_Name = models.CharField(max_length=20)
    Loser_First_Name = models.CharField(max_length=20)
    Loser_Last_Name = models.CharField(max_length=20)
    Winner_Score = models.IntegerField(choices=[(2,2)])
    Loser_Score = models.IntegerField(choices=[(x,x) for x in range(2)])
    Day = models.DateTimeField('date created', auto_now_add=True, editable=False)
    Points = models.IntegerField(editable=False, default=0)
    Winner_Rating = models.IntegerField(editable=False, default=0)
    Loser_Rating = models.IntegerField(editable=False, default=0)
    Updated = models.IntegerField(editable=False, default=0)

    def get_absolute_url(self):
        return "/ladder"

    class Meta:
        db_table = "matches"
        verbose_name_plural = "Matches"

    def __unicode__(self):
       return (self.Winner_Last_Name + " vs " + self.Loser_Last_Name)


class Practices(models.Model):
    Date = models.DateField(editable=False)
    Count = models.IntegerField(editable=False, default=0)

    def get_absolute_url(self):
        return "/attendance"

    class Meta:
        db_table = "practices"
        verbose_name_plural = "Practices"

    def __unicode__(self):
       return str(self.Date)

class AttendanceHistory(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Email = models.CharField(max_length=100, blank=True, help_text="Optional: Enter your email here if you wish to join the mailing list")
    Class_Standing = models.CharField(max_length=10, blank=True, help_text="Optional: Select your class standing", choices=[("Freshman", "Freshman"), ("Sophomore", "Sophomore"), ("Junior", "Junior"), ("Senior", "Senior"), ("Grad", "Grad")])
    Date = models.DateField(auto_now_add=True, editable=False)
    Time = models.DateTimeField('date created', auto_now_add=True, editable=False)
    Updated = models.IntegerField(editable=False, default=0)

    def get_absolute_url(self):
        return "/attendance"

    class Meta:
        db_table = "attendance_history"
        verbose_name_plural = "Club Attendance"

    def __unicode__(self):
       return str(self.Date) + ": " + self.First_Name + " " + self.Last_Name

class Updates(models.Model):
    Date = models.DateField()
    Message = models.CharField(max_length=200)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "updates"
        verbose_name_plural = "Updates"

    def __unicode__(self):
       return str(self.Date) + ": " + self.Message

class Slides(models.Model):
    Date = models.DateField()
    Title = models.CharField(max_length=100)

    ########## How to get the SlidesID ##########
    # Full URL = https://docs.google.com/presentation/d/1152Jzvxr-hDXlGE1zaT4_NuZf8sl-GAIvCUhhzMA800/edit#slide=id.g1b0ebe7be8_0_0
    # SlidesID = 1152Jzvxr-hDXlGE1zaT4_NuZf8sl-GAIvCUhhzMA800
    SlidesID = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/photos"

    class Meta:
        db_table = "slides"
        verbose_name_plural = "Slides"

    def __unicode__(self):
       return str(self.Title)

class EBoard(models.Model):
    Name = models.CharField(max_length=50)
    Position = models.IntegerField(choices=[(1, "President"), (2, "Co-President"), (3, "Treasurer"), (4, "Secretary"), (5, "Webmaster")])

    def get_absolute_url(self):
        return "/contact"

    class Meta:
        db_table = "eboard"
        verbose_name_plural = "EBoard"

    def __unicode__(self):
       return str(self.Name)

class Images(models.Model):
    BACKGROUND = 1
    HOME = 2
    ATTENDANCE = 3
    SUMMARY = 4
    LADDER = 5
    ABOUT = 6
    RULES = 7
    CONTACT = 8

    PAGE_CHOICES = (
        (BACKGROUND, "background"),
        (HOME, "home"),
        (ATTENDANCE, "attendance"),
        (SUMMARY, "summary"),
        (LADDER, "ladder"),
        (ABOUT, "about"),
        (RULES, "rules"),
        (CONTACT, "contact")
    )

    Page = models.IntegerField(choices=PAGE_CHOICES)
    URL = models.CharField(max_length=200)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "images"
        verbose_name_plural = "Images"

    def __unicode__(self):
       return str(self.get_Page_display())


class OrganizationInformation(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    Copyright_Year = models.CharField(max_length=20)
    Description = models.CharField(max_length=500)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "organization_information"
        verbose_name_plural = "Organization Information"

    def __unicode__(self):
       return str(self.Name)

class FrontPageContent(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "front_page_content"
        verbose_name_plural = "Front Page Content"

    def __unicode__(self):
       return str(self.Title)


class SocialMedia(models.Model):
    Website_URL = models.CharField(max_length=100)
    Logo_URL = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "social_media"
        verbose_name_plural = "Social Media"

    def __unicode__(self):
       return str(self.Website_URL)


class ColorScheme(models.Model):

    BINGHAMTONGREEN = '#005a43'
    INDIANRED = '#CD5C5C'
    LIGHTCORAL = '#F08080'
    SALMON = '#FA8072'
    DARKSALMON = '#E9967A'
    LIGHTSALMON = '#FFA07A'
    CRIMSON = '#DC143C'
    RED = '#FF0000'
    FIREBRICK = '#B22222'
    DARKRED = '#8B0000'
    PINK = '#FFC0CB'
    LIGHTPINK = '#FFB6C1'
    HOTPINK = '#FF69B4'
    DEEPPINK = '#FF1493'
    MEDIUMVIOLETRED = '#C71585'
    PALEVIOLETRED = '#DB7093'
    LIGHTSALMON = '#FFA07A'
    CORAL = '#FF7F50'
    TOMATO = '#FF6347'
    ORANGERED = '#FF4500'
    DARKORANGE = '#FF8C00'
    ORANGE = '#FFA500'
    GOLD = '#FFD700'
    YELLOW = '#FFFF00'
    LIGHTYELLOW = '#FFFFE0'
    LEMONCHIFFON = '#FFFACD'
    LIGHTGOLDENRODYELLOW = '#FAFAD2'
    PAPAYAWHIP = '#FFEFD5'
    MOCCASIN = '#FFE4B5'
    PEACHPUFF = '#FFDAB9'
    PALEGOLDENROD = '#EEE8AA'
    KHAKI = '#F0E68C'
    DARKKHAKI = '#BDB76B'
    LAVENDER = '#E6E6FA'
    THISTLE = '#D8BFD8'
    PLUM = '#DDA0DD'
    VIOLET = '#EE82EE'
    ORCHID = '#DA70D6'
    FUCHSIA = '#FF00FF'
    MAGENTA = '#FF00FF'
    MEDIUMORCHID = '#BA55D3'
    MEDIUMPURPLE = '#9370DB'
    REBECCAPURPLE = '#663399'
    BLUEVIOLET = '#8A2BE2'
    DARKVIOLET = '#9400D3'
    DARKORCHID = '#9932CC'
    DARKMAGENTA = '#8B008B'
    PURPLE = '#800080'
    INDIGO = '#4B0082'
    SLATEBLUE = '#6A5ACD'
    DARKSLATEBLUE = '#483D8B'
    MEDIUMSLATEBLUE = '#7B68EE'
    GREENYELLOW = '#ADFF2F'
    CHARTREUSE = '#7FFF00'
    LAWNGREEN = '#7CFC00'
    LIME = '#00FF00'
    LIMEGREEN = '#32CD32'
    PALEGREEN = '#98FB98'
    LIGHTGREEN = '#90EE90'
    MEDIUMSPRINGGREEN = '#00FA9A'
    SPRINGGREEN = '#00FF7F'
    MEDIUMSEAGREEN = '#3CB371'
    SEAGREEN = '#2E8B57'
    FORESTGREEN = '#228B22'
    GREEN = '#008000'
    DARKGREEN = '#006400'
    YELLOWGREEN = '#9ACD32'
    OLIVEDRAB = '#6B8E23'
    OLIVE = '#808000'
    DARKOLIVEGREEN = '#556B2F'
    MEDIUMAQUAMARINE = '#66CDAA'
    DARKSEAGREEN = '#8FBC8B'
    LIGHTSEAGREEN = '#20B2AA'
    DARKCYAN = '#008B8B'
    TEAL = '#008080'
    AQUA = '#00FFFF'
    CYAN = '#00FFFF'
    LIGHTCYAN = '#E0FFFF'
    PALETURQUOISE = '#AFEEEE'
    AQUAMARINE = '#7FFFD4'
    TURQUOISE = '#40E0D0'
    MEDIUMTURQUOISE = '#48D1CC'
    DARKTURQUOISE = '#00CED1'
    CADETBLUE = '#5F9EA0'
    STEELBLUE = '#4682B4'
    LIGHTSTEELBLUE = '#B0C4DE'
    POWDERBLUE = '#B0E0E6'
    LIGHTBLUE = '#ADD8E6'
    SKYBLUE = '#87CEEB'
    LIGHTSKYBLUE = '#87CEFA'
    DEEPSKYBLUE = '#00BFFF'
    DODGERBLUE = '#1E90FF'
    CORNFLOWERBLUE = '#6495ED'
    MEDIUMSLATEBLUE = '#7B68EE'
    ROYALBLUE = '#4169E1'
    BLUE = '#0000FF'
    MEDIUMBLUE = '#0000CD'
    DARKBLUE = '#00008B'
    NAVY = '#000080'
    MIDNIGHTBLUE = '#191970'
    CORNSILK = '#FFF8DC'
    BLANCHEDALMOND = '#FFEBCD'
    BISQUE = '#FFE4C4'
    NAVAJOWHITE = '#FFDEAD'
    WHEAT = '#F5DEB3'
    BURLYWOOD = '#DEB887'
    TAN = '#D2B48C'
    ROSYBROWN = '#BC8F8F'
    SANDYBROWN = '#F4A460'
    GOLDENROD = '#DAA520'
    DARKGOLDENROD = '#B8860B'
    PERU = '#CD853F'
    CHOCOLATE = '#D2691E'
    SADDLEBROWN = '#8B4513'
    SIENNA = '#A0522D'
    BROWN = '#A52A2A'
    MAROON = '#800000'
    WHITE = '#FFFFFF'
    SNOW = '#FFFAFA'
    HONEYDEW = '#F0FFF0'
    MINTCREAM = '#F5FFFA'
    AZURE = '#F0FFFF'
    ALICEBLUE = '#F0F8FF'
    GHOSTWHITE = '#F8F8FF'
    WHITESMOKE = '#F5F5F5'
    SEASHELL = '#FFF5EE'
    BEIGE = '#F5F5DC'
    OLDLACE = '#FDF5E6'
    FLORALWHITE = '#FFFAF0'
    IVORY = '#FFFFF0'
    ANTIQUEWHITE = '#FAEBD7'
    LINEN = '#FAF0E6'
    LAVENDERBLUSH = '#FFF0F5'
    MISTYROSE = '#FFE4E1'
    GAINSBORO = '#DCDCDC'
    LIGHTGRAY = '#D3D3D3'
    SILVER = '#C0C0C0'
    DARKGRAY = '#A9A9A9'
    GRAY = '#808080'
    DIMGRAY = '#696969'
    LIGHTSLATEGRAY = '#778899'
    SLATEGRAY = '#708090'
    DARKSLATEGRAY = '#2F4F4F'
    BLACK = '#000000'

    COLOR_CHOICES = (
        (BINGHAMTONGREEN, "BinghamtonGreen"),
        (INDIANRED, "Indianred"),
        (LIGHTCORAL, "Lightcoral"),
        (SALMON, "Salmon"),
        (DARKSALMON, "Darksalmon"),
        (LIGHTSALMON, "Lightsalmon"),
        (CRIMSON, "Crimson"),
        (RED, "Red"),
        (FIREBRICK, "Firebrick"),
        (DARKRED, "Darkred"),
        (PINK, "Pink"),
        (LIGHTPINK, "Lightpink"),
        (HOTPINK, "Hotpink"),
        (DEEPPINK, "Deeppink"),
        (MEDIUMVIOLETRED, "Mediumvioletred"),
        (PALEVIOLETRED, "Palevioletred"),
        (LIGHTSALMON, "Lightsalmon"),
        (CORAL, "Coral"),
        (TOMATO, "Tomato"),
        (ORANGERED, "Orangered"),
        (DARKORANGE, "Darkorange"),
        (ORANGE, "Orange"),
        (GOLD, "Gold"),
        (YELLOW, "Yellow"),
        (LIGHTYELLOW, "Lightyellow"),
        (LEMONCHIFFON, "Lemonchiffon"),
        (LIGHTGOLDENRODYELLOW, "Lightgoldenrodyellow"),
        (PAPAYAWHIP, "Papayawhip"),
        (MOCCASIN, "Moccasin"),
        (PEACHPUFF, "Peachpuff"),
        (PALEGOLDENROD, "Palegoldenrod"),
        (KHAKI, "Khaki"),
        (DARKKHAKI, "Darkkhaki"),
        (LAVENDER, "Lavender"),
        (THISTLE, "Thistle"),
        (PLUM, "Plum"),
        (VIOLET, "Violet"),
        (ORCHID, "Orchid"),
        (FUCHSIA, "Fuchsia"),
        (MAGENTA, "Magenta"),
        (MEDIUMORCHID, "Mediumorchid"),
        (MEDIUMPURPLE, "Mediumpurple"),
        (REBECCAPURPLE, "Rebeccapurple"),
        (BLUEVIOLET, "Blueviolet"),
        (DARKVIOLET, "Darkviolet"),
        (DARKORCHID, "Darkorchid"),
        (DARKMAGENTA, "Darkmagenta"),
        (PURPLE, "Purple"),
        (INDIGO, "Indigo"),
        (SLATEBLUE, "Slateblue"),
        (DARKSLATEBLUE, "Darkslateblue"),
        (MEDIUMSLATEBLUE, "Mediumslateblue"),
        (GREENYELLOW, "Greenyellow"),
        (CHARTREUSE, "Chartreuse"),
        (LAWNGREEN, "Lawngreen"),
        (LIME, "Lime"),
        (LIMEGREEN, "Limegreen"),
        (PALEGREEN, "Palegreen"),
        (LIGHTGREEN, "Lightgreen"),
        (MEDIUMSPRINGGREEN, "Mediumspringgreen"),
        (SPRINGGREEN, "Springgreen"),
        (MEDIUMSEAGREEN, "Mediumseagreen"),
        (SEAGREEN, "Seagreen"),
        (FORESTGREEN, "Forestgreen"),
        (GREEN, "Green"),
        (DARKGREEN, "Darkgreen"),
        (YELLOWGREEN, "Yellowgreen"),
        (OLIVEDRAB, "Olivedrab"),
        (OLIVE, "Olive"),
        (DARKOLIVEGREEN, "Darkolivegreen"),
        (MEDIUMAQUAMARINE, "Mediumaquamarine"),
        (DARKSEAGREEN, "Darkseagreen"),
        (LIGHTSEAGREEN, "Lightseagreen"),
        (DARKCYAN, "Darkcyan"),
        (TEAL, "Teal"),
        (AQUA, "Aqua"),
        (CYAN, "Cyan"),
        (LIGHTCYAN, "Lightcyan"),
        (PALETURQUOISE, "Paleturquoise"),
        (AQUAMARINE, "Aquamarine"),
        (TURQUOISE, "Turquoise"),
        (MEDIUMTURQUOISE, "Mediumturquoise"),
        (DARKTURQUOISE, "Darkturquoise"),
        (CADETBLUE, "Cadetblue"),
        (STEELBLUE, "Steelblue"),
        (LIGHTSTEELBLUE, "Lightsteelblue"),
        (POWDERBLUE, "Powderblue"),
        (LIGHTBLUE, "Lightblue"),
        (SKYBLUE, "Skyblue"),
        (LIGHTSKYBLUE, "Lightskyblue"),
        (DEEPSKYBLUE, "Deepskyblue"),
        (DODGERBLUE, "Dodgerblue"),
        (CORNFLOWERBLUE, "Cornflowerblue"),
        (MEDIUMSLATEBLUE, "Mediumslateblue"),
        (ROYALBLUE, "Royalblue"),
        (BLUE, "Blue"),
        (MEDIUMBLUE, "Mediumblue"),
        (DARKBLUE, "Darkblue"),
        (NAVY, "Navy"),
        (MIDNIGHTBLUE, "Midnightblue"),
        (CORNSILK, "Cornsilk"),
        (BLANCHEDALMOND, "Blanchedalmond"),
        (BISQUE, "Bisque"),
        (NAVAJOWHITE, "Navajowhite"),
        (WHEAT, "Wheat"),
        (BURLYWOOD, "Burlywood"),
        (TAN, "Tan"),
        (ROSYBROWN, "Rosybrown"),
        (SANDYBROWN, "Sandybrown"),
        (GOLDENROD, "Goldenrod"),
        (DARKGOLDENROD, "Darkgoldenrod"),
        (PERU, "Peru"),
        (CHOCOLATE, "Chocolate"),
        (SADDLEBROWN, "Saddlebrown"),
        (SIENNA, "Sienna"),
        (BROWN, "Brown"),
        (MAROON, "Maroon"),
        (WHITE, "White"),
        (SNOW, "Snow"),
        (HONEYDEW, "Honeydew"),
        (MINTCREAM, "Mintcream"),
        (AZURE, "Azure"),
        (ALICEBLUE, "Aliceblue"),
        (GHOSTWHITE, "Ghostwhite"),
        (WHITESMOKE, "Whitesmoke"),
        (SEASHELL, "Seashell"),
        (BEIGE, "Beige"),
        (OLDLACE, "Oldlace"),
        (FLORALWHITE, "Floralwhite"),
        (IVORY, "Ivory"),
        (ANTIQUEWHITE, "Antiquewhite"),
        (LINEN, "Linen"),
        (LAVENDERBLUSH, "Lavenderblush"),
        (MISTYROSE, "Mistyrose"),
        (GAINSBORO, "Gainsboro"),
        (LIGHTGRAY, "Lightgray"),
        (SILVER, "Silver"),
        (DARKGRAY, "Darkgray"),
        (GRAY, "Gray"),
        (DIMGRAY, "Dimgray"),
        (LIGHTSLATEGRAY, "Lightslategray"),
        (SLATEGRAY, "Slategray"),
        (DARKSLATEGRAY, "Darkslategray"),
        (BLACK, "Black"),
    )

    HeaderColor = models.CharField(choices=COLOR_CHOICES, max_length=30)
    HeaderTextColor = models.CharField(choices=COLOR_CHOICES, max_length=30)
    BodyTextColor = models.CharField(choices=COLOR_CHOICES, max_length=30)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "color_scheme"
        verbose_name_plural = "Color Scheme"

    def __unicode__(self):
       return str(self.get_HeaderColor_display())