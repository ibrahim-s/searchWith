# Search With (Пошук за допомогою) #

* Автор: Ibrahim Hamadeh
* Завантажити [стабільну версію][1]
* Сумісність з NVDA: 2019.3 та новіші

Цей додаток використовується для пошуку тексту за допомогою різних пошукових
систем. Навіть, якщо не буде виділено жодного тексту, після натискання жесту
додатка відкриється діалог з полем редагування для введення пошукового
запиту, для пошуку за допомогою Google натисніть клавішу enter, а для пошуку
за допомогою інших систем натисніть клавішу tab.

І якщо вам потрібно знайти виділений текст, виділіть текст і натисніть один
раз, після чого з’явиться меню з можливістю вибрати різні пошукові
системи. Щоб шукати виділений текст безпосередньо в Google, натисніть цю
комбінацію двічі.

The Default gesture for the addon is: NVDA+ Windows+ S. If the keystroke do not work for you, or conflict with other keystroke, you can as always add a gesture or change the existent one going to: NVDA menu>preferences>inputGestures>Search With category.

## Використання

* If you want to enter a search query, just press the addon gesture. A
  dialog will be displayed, with an edit field to enter the search term.
* Want to search with Google? just press enter.
* Otherwise tab to Other Engines button, and give it a space, a popup menu
  will show up, with various search engines to choose. Yahoo, Bing,
  DuckDuckGo, and Youtube. This is the default menu, and you may modify it
  from addon's setting panel.
* Another way to use the addon, is by selecting some text. And on Pressing
  the addon's gesture, or any other you have assigned to it, a virtual menu
  will be displayed with various search engines, either the default menu, or
  any other you have tailed to your needs.
* Виберіть одну з них і натисніть клавішу enter, відкриється основний
  браузер з результатами пошуку. або, якщо ви хочете здійснювати пошук
  безпосередньо в Google, натисніть жест двічі, і все готово.
* Want to trigger search menu specifically for clipboard or last spoken
  text? OK, then you can from input gestures dialog, assigned a gesture for:
    * Trigger search menu for clipboard text, and pressed twice searches
      that text by Google directly.
    * Trigger search menu for last spoken text, and pressed twice searches
      that text by Google directly.
* Want to modify Search with menu? Yes you can do that from the setting
  panel, and adjust the menu to fit to your mood and needs.
* You can from there, add to Search with menu, other available search
  engines. And you can if you like, remove an item from it, move item up,
  move item down, or return and set menu to default state.
* Якщо ви хочете, щоб ці зміни були постійними, вам потрібно зберегти
  конфігурацію після внесених змін.
* Хочете шукати в Google, використовуючи інші мовні параметри?
* Потім перейдіть до категорії «Пошук за допомогою» в панелі налаштувань, у
  вікні зі списком ви можете вибрати пошук у Google:

    1. Використовувати налаштування браузера та мови.
    2. Використовувати мову NVDA.
    3. Використовувати мову Windows.

* Moreover, you have the option to choose the default query in Search with
  dialog. From the Options for default query combo box in setting panel, you
  can choose either

    * Leave blank
    * Use clipboard text
    * Use last spoken text

* And if clipboard or last spoken text is chosen, text in search box will be
  displayed selected, so that you can easily override it.
* Lastly, especially for advanced users
* You can through a check box in setting panel, choose if you want to
  preserve your data folder upon installing a new version. Be aware,
  choosing that you will not get new search engines, if any were included in
  the new addon version.
And that's it, hope to search for good and find it, happy searching!

### Changes for 2.0 ###

* Disable the addon in secure mode.
* Update last tested version to 2022.1, to comply with recent addon api
  version.

### Changes for 1.8 ###

* Add a check box in setting panel, to let advanced users preserve their
  data folder.
* Add two new entries in input gestures:
    * trigger search menu for clipboard text, press twice searches Google
      directly.
    * Trigger search menu for last spoken text, press twice searches Google
      directly.

### Changes for 1.7

* Make a combo box in addon's setting, to choose an option for default query
  in search with dialog.
* You can select either Leave blank, Use clipboard text, or Use last spoken
  text.

### Зміни у версії 1.2

* У меню додано інші сайти, такі як Stackoverflow, Stackexchange,
  GoogleBooks та інші.
* Додано параметр для використання останнього промовленого тексту як
  початкового запиту у діалозі додатка «Пошук за допомогою».

### Зміни у версії 0.4

* Додано діалог для введення пошукового запиту в разі, якщо немає виділеного
  дексту.
* Make possible to modify Search with menu from setting panel, to fit to
  user needs.

### Зміни у версії 0.3

* Додано панель налаштувань, яка надає більше мовних параметрів у пошуку
  Google.

### Зміни у версії 0.1

* Перша версія

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=searchwith
