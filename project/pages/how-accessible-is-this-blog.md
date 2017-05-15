title: How accessible is this blog?
date: 2017-03-24 14:00:00
type: post


<br>To understand web accessibility better, I decided to audit my own blog.  The blog is small (at time of writing four pages including the main page!),
but I am interested to see what kinds of issues come up even before adding complicated features and substantial content to a site.
<br>
<br>
<br>

###How will I do the audit?
<br>I decided on the following steps:
<br>

1) Test using the pa11y command line tool and review the feedback it provides<br>
2) Check the color contrast using the webaim tool<br>
3) Navigate the site using only a keyboard<br>
4) Assess the site using a screen reader emulator<br>
5) Conclusion and improvements to make<br>
<br>
<br>
<br>


###1) Test using the pa11y command line tool and review the feedback it provides

<br>On the main page of my blog, the pa11y [command line tool](https://github.com/pa11y/pa11y) found:<br>
6 Errors<br>
1 Warnings<br>
8 Notices<br>
<br>
The notices were things like:

`Notice: Check that the title element describes the document.`<br>
`   WCAG2AA.Principle2.Guideline2_4.2_4_2.H25.2`<br>
`   html > head > title`<br>
`   <title>Nasreen's blog</title>`<br>

<br>None of them require changes - they are things that it is easy for a human reading the notices to check
but impossible for a computer program to know.  The tool is designed to give feedback as a guide for improvements.
Including notices like this means that is can direct attention to possible issues beyond
the scope of definitive automated testing, which could be very helpful.

<br>The warning was:<br>

`Warning: The heading structure is not logically nested. This h4 element should be an h2 to be properly nested.`<br>
`   WCAG2AA.Principle1.Guideline1_3.1_3_1_A.G141`<br>
`   #body > div > div > div > div > h4`<br>
`   <h4>Posts :</h4>`<br>


<br>This should be changed - the posts subheading should be a h2 element.  There is not much content on this page, if there was more content illogical document structure could make navigation very [frustrating for screen readers to use](http://academics.georgiasouthern.edu/col/web-accessibility/accessibility-document-structure/).

<br>There were two kinds of errors.  One requires a lang attribute to be added to the html tag.

<br>The others indicated empty links, like this:

`Error: Anchor element found with a valid href attribute, but no link content has been supplied.`<br>
`    WCAG2AA.Principle4.Guideline4_1.4_1_2.H91.A.NoContent`<br>
`    #body > div > div > div > div > a`<br>
`    <a href="/mutable-default-parameters/"> </a>`<br>


<br>It seems like these are caused by ::after pseudo-elements being automatically added by flask.  This is something I want to learn more about, as there shouldn't be empty links.
<br>
<br>
<br>

###2) Check the contrast using the webaim tool

<br>The [webaim tool](http://wave.webaim.org/) gives information about [contrast errors](http://webaim.org/resources/contrastchecker/).  It also gives other kinds of errors, which verified the feedback from the pa11y tool.

<br>The contrast between the text and the background is very low; the body text color is too light to pass the contrast test (the larger text passed because less contrast is required for larger text to be clear).  The tool also allowed me to find an appropriate color; it is currently #808080, #515151 is a similar shade which gives better contrast.
<br>
<br>
<br>

###3) Navigate the site using only a keyboard
<br>I navigated through my blog using tab, alt&tab (to go back), and enter (to select).  This was straightforward because there are only a few pages.
<br>
<br>
<br>

###4) Assess the site using a screen reader emulator

<br>I used an addon for fire called [fangs](https://addons.mozilla.org/en-US/firefox/addon/fangs-screen-reader-emulator/contribute/roadblock/?src=search&version=1.0.8.1-signed.1-signed)

<br>The output it gave for the main pages is:
<br>"Page has two headings and seven links Nasreens's blog dash Internet Explorer Heading level one A blog by Nasreen Heading level four Posts colon List of two items bullet Link Three weeks at RC dash some reflections bullet LInk Mutable Default Parameters in Python Lists end Link Link Link Link Link"

<br>This highlights the need to remove the empty links from the site.
<br>
<br>
<br>

###5) Conclusion and improvements to make

<br>Even though my site is very small, I still found improvements to make.  This really highlights to me how easy it is to overlook web accessibility, either through lack of knowledge or planning.  I think to overcome this, it's important to keep finding out more and sharing knowledge.

<br>The tools I used were all informative and easy to use.

<br>Improvements to make to my site:
<br>- change h4 element to h2
<br>- investigate pseudo-elements with empty links
<br>- change the body font color from #808080 to #515151
<br>- add the missing lang attribute

<br>
<br>
