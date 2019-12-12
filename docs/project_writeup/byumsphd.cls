% BYU MS/PhD LaTeX Class File
%
% Copyright (c) 2006 Christopher K. Monson
% The latest version of this file may be obtained from
%   http://latex-byu-thesis.googlecode.com/
%
% Bug reports are also welcome at that address, and will be addressed as
% quickly as possible; I know that this is your baby and that everyone is on a
% tight schedule.  I was there once.
%
% License: LaTeX Project Public License (www.latex-project.org/lppl.txt)
%   Executive summary:
%       This software is copyright but you are granted a license which gives
%       you, the "user" of the software, legal permission to copy, distribute,
%       and/or modify the software. However, if you modify the software and
%       then distribute it (even just locally) you must change the name of the
%       software to avoid confusion.
%
% OR (dual-licensed)
%
% License: GNU Lesser General Public License (www.gnu.org/licenses/lgpl.html)
%
% Author Information:
%   Christopher K. Monson
%   Brigham Young University
%   monpublic@gmail.com
%
% Please contact the author for change requests.  If you have patches, please
% send those to the author as well so that this class has a single point of
% distribution and all may benefit.
%
% NOTE TO USERS WHO DON'T USE NATBIB:
%
% Your references section may or may not be included properly in the table of
% contents or in the pdf bookmarks.  If it isn't, do the following in the
% preamble of your document and it should show up there.:
%
% \let\old@openbib@code\@openbib@code
% \renewcommand{\@openbib@code}{\addcontentsline{toc}{chapter}{\bibname}\old@openbib@code}
%
% Version: 1.4
%
% Changelog:
%   Chris Tensmeyer (2019-04-01):
%       *   Fix Vertical Spacing on first page to match template
%   Daron Barnes (2017-07-12):
%       *   Removed Month-Year of graduation from title page.
%   Andrew McNabb (2013-06-05):
%       *   Bump version to 1.5
%       *   Change monthgraduated to monthapproved (issue 48)
%       *   Make the electronic option set openany (issue 48)
%   Andrew McNabb (2012-03-02):
%       *   Bumped version to 1.4
%       *   Change to 11 pt and single spacing in the byuprop class.
%   Andrew McNabb (2012-03-02):
%       *   Bumped version to 1.3
%       *   Make abstracts in the byuprop class match the byumsphd class.
%   Andrew McNabb (2012-03-02):
%       *   Bumped version to 1.2.2
%       *   Ensure the Table of Contents name in the PDF bookmarks matches.
%       *   Work around a fatal error occuring with some versions of natbib.
%   Chris Monson (2011-04-18):
%       *   Bumped version to 1.2.1
%       *   More clarity on shifting requirements for abstracts (issue 38).
%       *   Made electronic option the default in the example file, clarified
%               use of geometry package.
%   Chris Monson (2011-03-11):
%       *   Bumped version to 1.2.0
%       *   New university requirements, per issue 37 (no sig page, no margin
%               shifting on electronic copies)
%       *   Backed out addition of driverfallback option in example - it is not
%               available on all systems.
%   Chris Monson (2011-03-03):
%       *   Bumped version to 1.1.9
%       *   Subtitle now works properly
%       *   Thanks to Oliver Kopp for microtype patch to the example file.
%   Chris Monson (2010-10-08):
%       *   Bumped version to 1.1.8
%       *   issue 31: example needs plainpages=false in hyperref settings
%   Chris Monson (2010-03-10):
%       *   Bumped version to 1.1.7
%       *   issue 27: Added bib.bib to the distribution tarball
%   Chris Monson (2010-03-10):
%       *   Bumped version to 1.1.6
%       *   issue 29: Removed deprecated commands from example file
%   Chris Monson (2010-01-06):
%       *   Bumped version to 1.1.5
%       *   Removed tocloft documentation until it can be better supported
%       *   Added twosidetoc option to the class
%   Chris Monson (2009-12-17):
%       *   Bumped version to 1.1.4
%       *   Added documentation about how to add dot leaders to the TOC, fixed
%           some spacing.
%   Chris Monson (2009-11-24):
%       *   Bumped version to 1.1.3
%       *   Fixed hardcopy option to work properly
%   Chris Monson (2009-11-23):
%       *   Bumped version to 1.1.2
%       *   issue 21: Make compliant headings the default
%       *   issue 22: Add convenience options for electronic/hardcopy
%   Chris Monson (2009-11-20):
%       *   Bumped version to 1.1.1
%       *   issue 19: ms setting gives "no line here to end" errors
%       *   issue 18: change monthsubmitted to monthgraduated
%       *   issue 20: page numbering wrong for chapter 1 in some cases
%       *   issue 17: bookmarks need to be numbered - see example file
%   Chris Monson (2009-11-14):
%       *   Bumped version to 1.1.0
%       *   Change Graduate Coordinator default to Kent E. Seamons
%       *   Addressed issue 16: template is out of sync with new university
%           requirements
%       *   Changed the canonical location in the comments (googlecode)
%       *   Added options for more margin fiddling
%   Chris Monson (2009-10-27):
%       *   Bumped version to 1.0.13
%       *   Addressed issue 12: chapter heading styles have changed
%       *   Addressed issue 13: lol, lot, and lof not linking properly
%       *   Made bibsection hack part of standard behavior
%   Chris Monson (2009-09-25):
%       *   Bumped version to 1.0.12
%   Lloyd Brown (Contrib) (2009-09-25):
%       *   Added options to enable "list of listings", named "lol".
%   Chris Monson (2009-09-16):
%       *   Bumped version to 1.0.11
%       *   Updated example file to be more informative.
%   Chris Monson (Anonymous Contrib) (2009-03-06):
%       *   Bumped version to 1.0.10
%       *   Added \copyrighttext settable option (replacing All Rights
%           Reserved)
%   Chris Monson (2008-05-21):
%       *   Bumped version to 1.0.9
%   Lloyd Brown (Contrib) (2008-05-15):
%       *   Added option for setting "Department" as in "Accepted for the
%           Department" to something else
%       *   Added option for setting "Graduate Coordinator" title to something
%           else
%       *   This closes issue 8 in the tracker
%   Chris Monson (2007-07-06):
%       *   Bumped version to 1.0.8
%       *   Fixed signature page to be compliant with new rules
%       *   Added duplexprinter convenience option
%       *   Added tocbibind to the example file to show people how to get their
%           bibliography referenced in the TOC
%       *   This closes issues 4 and 6 in the tracker
%   Chris Monson (2007-03-10):
%       *   Bumped version to 1.0.5
%       *   Addressed issue (2) on code.google.com/p/latex-byu-thesis as follows
%       *   Created a fake pdfbookmark command that switches on with hyperref
%       *   Inserted pdfbookmark commands per Dan Delorey (new requirements)
%       *   Later bumped version to 1.0.6
%       *   Added an option to put an entry for References into the TOC
%       *   Later bumped version to 1.0.7
%       *   Reverted the addition of refintoc.  There is an easier way in the
%           document itself, and it is too dependent on the particular
%           bibliography environment used.
%   Chris Monson (2007-03-09):
%       *   Bumped version to 1.0.4
%       *   Added the LGPL as an alternate license
%   Chris Monson (2007-02-01):
%       *   Created a version number and bumped it to 1.0.3
%       *   Added option for setting "Department of" string to something else
%   Chris Monson (2006-03-13):
%       *   Removed some cruft
%       *   Established some suitable defaults
%   Chris Monson (2006-03-10):
%       *   First reasonable release
%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{byumsphd}[2007/03/10 BYU LaTeX MS/PhD Class]
%
% Boolean option creation
\newif\if@hardcopyoption % tells us that the hardcopy option was set
\newif\if@electronicoption % tells us that the electronic option was set
\newif\if@twosidetoc % Two-sided printing starts at TOC (earlier than body)
\newif\if@simplechapterheading % "1 Title" instead of "Chapter 1<nl>Title"
\newif\if@thesis % generates \if@thesis, \@thesistrue, and \@thesisfalse
\newif\if@chapternum % for putting page numbers on part and chapter pages
\newif\if@centerchapter % for centered chapter headings vs. left-justified
\newif\if@vcenterpart % for vertical centering of parts vs. top
\newif\if@compliantsizes % for headings no larger than 12 pt (ugly)
\newif\if@lof % Show list of figures?
\newif\if@lot % Show list of tables?
\newif\if@lol % Show list of listings?
\newif\if@needdrawing % Need the eso-pic environment?  Drawing something?
\newif\if@needlistings % Need the listings package?  Using List of Listings?
\newif\if@layout % This will draw lines showing all the margins
\newif\if@equalmargins % Make all margins equal
\newif\if@grid % Show a grid
\newif\if@separator % Show a separator page between the single-sided and double-sided parts of the document
\newif\if@committeemembera
\newif\if@committeememberb
\newif\if@committeememberc
\newif\if@committeememberd
\newif\if@duplexprinter % Ensure that there are an even number of pages in the front matter

% committee members are not assumed to exist
\@committeememberafalse
\@committeememberbfalse
\@committeemembercfalse
\@committeememberdfalse

\newcommand{\@@sideval}{twoside}
\newcommand{\@@openval}{openright}
\newcommand{\@@ptsize}{12pt}

% This is an empty no-op command in case pdfbookmark is not defined (hyperref
% not included)
\newcommand{\@@pdfbookmark}[3][1]{%
  \ifx\pdfbookmark\undefined
    \relax
  \else
    \pdfbookmark[#1]{#2}{#3}%
  \fi
}%

%
% This document can serve as either a PhD dissertation or a Master's thesis
\DeclareOption{hardcopy}{\@hardcopyoptiontrue}
\DeclareOption{electronic}{\@electronicoptiontrue}
\DeclareOption{simplechapterheading}{\@simplechapterheadingtrue}
\DeclareOption{compliantheadings}{\@compliantsizestrue}
\DeclareOption{prettyheadings}{\@compliantsizesfalse}
\DeclareOption{chaptercenter}{\@centerchaptertrue}
\DeclareOption{chapterleft}{\@centerchapterfalse}
\DeclareOption{partmiddle}{\@vcenterparttrue}
\DeclareOption{parttop}{\@vcenterpartfalse}
\DeclareOption{ms}{\@thesistrue}
\DeclareOption{phd}{\@thesisfalse}
\DeclareOption{chapternum}{\@chapternumtrue}
\DeclareOption{nochapternum}{\@chapternumfalse}
\DeclareOption{lof}{\@loftrue}
\DeclareOption{lot}{\@lottrue}
\DeclareOption{lol}{\@needlistingstrue \@loltrue}
\DeclareOption{layout}{\@needdrawingtrue \@layouttrue}
\DeclareOption{grid}{\@needdrawingtrue \@gridtrue}
\DeclareOption{separator}{\@separatortrue}
\DeclareOption{duplexprinter}{\@duplexprintertrue}
\DeclareOption{twoside}{\renewcommand{\@@sideval}{twoside}}%
\DeclareOption{oneside}{\renewcommand{\@@sideval}{oneside}}%
\DeclareOption{equalmargins}{\@equalmarginstrue}%
\DeclareOption{openright}{\renewcommand{\@@openval}{openright}}%
\DeclareOption{openany}{\renewcommand{\@@openval}{openany}}%
\DeclareOption{twosidetoc}{\@twosidetoctrue}%
\DeclareOption{10pt}{\renewcommand{\@@ptsize}{10pt}}%
\DeclareOption{11pt}{\renewcommand{\@@ptsize}{11pt}}%
\DeclareOption{12pt}{\renewcommand{\@@ptsize}{12pt}}%
% Ignore the letterpaper option, but allow it to be passed.
\DeclareOption{letterpaper}{\typeout{Ignoring option ``letterpaper''}}%

\setlength{\unitlength}{1in}
%
% Default to compliant heading sizes
\@compliantsizestrue
% Default to not using the convenience settings for hardcopy or ETD
\@hardcopyoptionfalse
\@electronicoptionfalse
% Default to two-sided printing starting at the body (not TOC)
\@twosidetocfalse
% Default to equal margins
\@equalmarginstrue
% Default to NOT indenting first paragraph, using normal chapter headings
\@simplechapterheadingfalse
% Default to NOT showing lists of figures and tables
\@loffalse
\@lotfalse
\@lolfalse
% Default to PhD
\@thesisfalse
% Default to one-sided printing
\@duplexprinterfalse
% Don't show the layout, usually
\@needdrawingfalse
\@layoutfalse
\@gridfalse
\ExecuteOptions{%
    chapternum,
    chapterleft,
    partmiddle,
    equalmargins,
    oneside,
    }%
\ProcessOptions
%
% Handle convenience settings
\if@hardcopyoption
    \if@electronicoption
        \ClassError{byumsphd}{%
            Invalid inclusion of both ``electronic'' and ``hardcopy''
            in class options.}%
    \fi
    \@equalmarginsfalse
    \renewcommand{\@@sideval}{twoside}
\fi
\if@electronicoption
    \@equalmarginstrue
\fi
%
% We base our work on the report class
%
% You would think that we could just use a DeclareOption* and pass the options
% on to this class, but that doesn't work very well.  If you want to do that,
% you can't use ExecuteOptions to set defaults because then the overriding
% options never get passed.  It's nuts.  So, this is how we do it, with
% appropriate default specifications.
\LoadClass[\@@ptsize,letterpaper,\@@sideval,\@@openval]{report}
%
% Rather than fiddle with spacing, we set it up using the setspace package
% Note that even though most of the document is double spaced, we start with
% single spacing because of the following reasons:
%  * setspace likes to *enlarge* the spacing, not shrink it
%  * the minimum style requirements dictate vertical spacing as a number of
%   ``blank lines'', and the size of those lines is single-spaced.
\RequirePackage[singlespacing]{setspace}
%
% The geometry package is great and we use it rather than fiddling with the
% margins directly.  We do have to employ some margin-fiddling trickery after
% the preamble, however, because the geometry package does not provide a way to
% set the margins in the middle of a document.
\RequirePackage{geometry}
%
% If we are showing a list of listings, then we need to include the listings package
\if@needlistings
    \RequirePackage{listings}%
\fi
%
% If we are showing layout grids, then we include the appropriate package and
% draw stuff on every page.
\if@needdrawing
    \RequirePackage[grid=false]{eso-pic}%
    \newcommand{\@vertline}{\line(0,1){11}}
    \newcommand{\@horzline}{\line(1,0){8.5}}
    \newcommand{\@maingrid}{%
        \multiput(1,0)(1,0){8}{\thicklines\@vertline}%
        \multiput(0,1)(0,1){10}{\thicklines\@horzline}%
    }%
    \newcommand{\@smallgrid}{%
        \multiput(0.5,0)(1,0){8}{\thinlines\@vertline}%
        \multiput(0,0.5)(0,1){11}{\thinlines\@horzline}%
    }%
    \newcommand{\@layoutpreamble}{\setlength{\unitlength}{1in}}
    \newcommand{\@rightsidebox}{
        \put (1.5,1){\dashbox{0.03125}(6,9)}%
    }%
    \newcommand{\@leftsidebox}{
        \put (1,1){\dashbox{0.03125}(6,9)}%
    }%
    \newcommand{\@prefaceinnerbox}{
        \put (1.5,1){\dashbox{0.03125}(6,8)}%
    }%
    \AddToShipoutPicture{%
        \@layoutpreamble
        \if@layout
            \@rightsidebox
            \@leftsidebox
            \@prefaceinnerbox
        \fi
        \if@grid
            \@smallgrid
            \@maingrid
        \fi
    }%
\fi
% Name of the degree
\newcommand*{\@degreename}{%
    \if@thesis%
        Master of Science%
    \else%
        Doctor of Philosophy%
    \fi%
}%
%
% Name of document
\newcommand*{\@documenttype}{%
    \if@thesis%
        project%
    \else%
        dissertation%
    \fi%
}%
%
% Page style for initial chapter and part pages
\newcommand*{\@chapterpagestyle}{%
    \if@chapternum%
        \thispagestyle{plain}%
    \else%
        \thispagestyle{empty}%
    \fi%
}%
%
% Tells the chapter headings how to justify themselves (center or left)
\newenvironment{@headjustify}{%
    \begingroup
    \if@centerchapter
        \centering
    \fi
}{%
    \endgroup
}%
%
% Sets the top spacing for a Part
\newcommand{\@parttopspace}{%
    \if@vcenterpart
        \vspace*{\fill}\par
    \else
        \begin{singlespace}%
            \vspace*{\@prefacemargingapsingle}\par
        \end{singlespace}%
    \fi
}%
%
% Sets the bottom spacing for a Part
\newcommand{\@partbottomspace}{%
    \if@vcenterpart
        \vspace*{\fill}\par
    \else
        \begin{singlespace}%
            \vspace*{3\@blankline}\par
        \end{singlespace}%
    \fi
}%
%
% Use this instead of \Large in case compliant sizes are needed
\newcommand{\@sizeLarge}{%
    \if@compliantsizes
        \normalsize
    \else
        \Large
    \fi
}%
%
% Use this instead of \large in case compliant sizes are needed
\newcommand{\@sizelarge}{%
    \if@compliantsizes
        \normalsize
    \else
        \large
    \fi
}%
%
% Use this instead of \Huge in case compliant sizes are needed
\newcommand{\@sizeHuge}{%
    \if@compliantsizes
        \normalsize
    \else
        \Huge
    \fi
}%
%
% Use this instead of \huge in case compliant sizes are needed
\newcommand{\@sizehuge}{%
    \if@compliantsizes
        \normalsize
    \else
        \huge
    \fi
}%
%
\newcommand{\@clearemptydoublepage}{%
    \clearpage
    {\pagestyle{empty}\cleardoublepage}%
}%
%
\newcommand{\clearpage@forchapter}{%
    \if@openright
        \cleardoublepage
    \else
        \clearpage
    \fi
}%
%
% These are internal variables used throughout the class.  They represent
% default values for their corresponding @-less versions.
\newcommand{\@university}{Brigham Young University}
\newcommand{\@universityabbrev}{BYU}
\newcommand{\@department}{Computer Science}
\newcommand{\@departmentprefix}{Department of}
\newcommand{\@departmentprefixshort}{Department}
\newcommand{\@graduatecoordinator}{Kent~E.~Seamons}
\newcommand{\@graduatecoordinatortitle}{Graduate~Coordinator}
\newcommand{\@college}{College of Physical and Mathematical Sciences}
\newcommand{\@collegedean}{Thomas~W.~Sederberg}
\newcommand{\@collegedeantitle}{Associate Dean}
\newcommand{\@committeechair}{}
\newcommand{\@committeemembera}{}
\newcommand{\@committeememberb}{}
\newcommand{\@committeememberc}{}
\newcommand{\@committeememberd}{}
\newcommand{\@monthgraduated}{}
\newcommand{\@yeargraduated}{}
\newcommand{\@yearcopyrighted}{\@yeargraduated}
\newcommand{\@copyrighttext}{All Rights Reserved}
%
\newcommand{\@documentabstract}{}
\newcommand{\@documentkeywords}{}
\newcommand{\@acknowledgments}{}
\newcommand{\@bindingoffset}{0.5in}
%
% This tells us whether to generate document keywords
\newif\if@hasdocumentkeywords
\@hasdocumentkeywordsfalse
%
% This tells us whether to generate the acknowledgments
\newif\if@hasacknowledgments
\@hasacknowledgmentsfalse
%
% Set up default geometry specifications
\geometry{top=1.0in,
          bottom=1.0in,
          textwidth=6.5in,
          hcentering}
\if@equalmargins
    \geometry{bindingoffset=0in}
\else
    \geometry{bindingoffset=\@bindingoffset}
\fi
%
% Here are some things that can be set from inside the document.  Most of them
% have suitable defaults.
\newcommand{\university}[1]{\renewcommand{\@university}{#1}}
\newcommand{\universityabbrev}[1]{\renewcommand{\@universityabbrev}{#1}}
\newcommand{\department}[1]{\renewcommand{\@department}{#1}}
\newcommand{\departmentprefix}[1]{\renewcommand{\@departmentprefix}{#1}}
\newcommand{\departmentprefixshort}[1]{\renewcommand{\@departmentprefixshort}{#1}}
\newcommand{\graduatecoordinator}[1]{\renewcommand{\@graduatecoordinator}{#1}}
\newcommand{\graduatecoordinatortitle}[1]{\renewcommand{\@graduatecoordinatortitle}{#1}}
\newcommand{\college}[1]{\renewcommand{\@college}{#1}}
\newcommand{\collegedean}[1]{\renewcommand{\@collegedean}{#1}}
\newcommand{\collegedeantitle}[1]{\renewcommand{\@collegedeantitle}{#1}}
\newcommand{\committeechair}[1]{\renewcommand{\@committeechair}{#1}}
\newcommand{\committeemembera}[1]{\@committeememberatrue\renewcommand{\@committeemembera}{#1}}
\newcommand{\committeememberb}[1]{\@committeememberbtrue\renewcommand{\@committeememberb}{#1}}
\newcommand{\committeememberc}[1]{\@committeememberctrue\renewcommand{\@committeememberc}{#1}}
\newcommand{\committeememberd}[1]{\@committeememberdtrue\renewcommand{\@committeememberd}{#1}}
\newcommand{\monthsubmitted}[1]{\ClassWarning{byumsphd}{monthsubmitted is deprecated - use monthgraduated instead}\monthgraduated{#1}}% TODO: delete this
\newcommand{\yearsubmitted}[1]{\ClassWarning{byumsphd}{yearsubmitted is deprecated - use yeargraduated instead}\yeargraduated{#1}}% TODO: delete this
\newcommand{\monthgraduated}[1]{\renewcommand{\@monthgraduated}{#1}}
\newcommand{\yeargraduated}[1]{\renewcommand{\@yeargraduated}{#1}}
\newcommand{\yearcopyrighted}[1]{\renewcommand{\@yearcopyrighted}{#1}}
\newcommand{\copyrighttext}[1]{\renewcommand{\@copyrighttext}{#1}}
%
\newcommand{\documentabstract}[1]{\renewcommand{\@documentabstract}{#1}}
\newcommand{\documentkeywords}[1]{%
    \@hasdocumentkeywordstrue
    \renewcommand{\@documentkeywords}{#1}%
}
\newcommand{\acknowledgments}[1]{%
    \@hasacknowledgmentstrue
    \renewcommand{\@acknowledgments}{#1}%
}
\newcommand{\setbindingoffset}[1]{%
    \renewcommand{\@bindingoffset}{#1}%
    \if@equalmargins\else
        \geometry{bindingoffset=#1}%
    \fi
}
\newcommand{\settextwidth}[1]{\geometry{textwidth=#1}}
%
% Internal lengths with no external settings
\newlength{\@assumedcharwidth}
\newlength{\@defaultindent}
\newlength{\@blankline}
\newlength{\@prefacemargingapsingle}
\newlength{\@prefacemargingapdouble}
\setlength{\@assumedcharwidth}{6pt}
\setlength{\@defaultindent}{6\@assumedcharwidth}
\setlength{\@blankline}{\baselineskip}
%
% This is the margin gap between the top of the paper and single-spaced text.  It defines a margin that is a total of 2 inches from the top
\setlength{\@prefacemargingapsingle}{1in}
\setlength{\@prefacemargingapdouble}{\@prefacemargingapsingle}
\addtolength{\@prefacemargingapdouble}{-\baselineskip}
%
% This is defined for a gap that goes from the top of the page down to text
% that is double-spaced.  Because double-spacing text moves the text down
% within a double-space height box, it makes the margins look wrong (even
% though they are technically right).  Subtracting a single-space height fixes
% the problem in these cases.

%\end{doublespace}
%
% Title page
\renewcommand{\titlepage}{%
    \clearpage
    \@@pdfbookmark[1]{Title Page}{title}%
    {\parindent 0pt%
    {\centering
    \parbox[t]{5in}{\centering
        \begin{doublespace}%
            \@title
        \end{doublespace}%
    \par}%
    \vfill
        \@author
    \vfill
        A {\@documenttype} submitted to the faculty of\\%
        \@university\\%
        in partial fulfillment of the requirements for the degree of\\%
        \begin{doublespace}
            \@degreename
        \end{doublespace}
    \vfill
        \@committeechair, Chair\\%
        \if@committeemembera
            \@committeemembera\\%
        \fi
        \if@committeememberb
            \@committeememberb\\%
        \fi
        \if@committeememberc
            \@committeememberc\\%
        \fi
        \if@committeememberd
            \@committeememberd\\%
        \fi
    \vfill
    %\vfill
        \begin{doublespace}%
            {\@departmentprefix} {\@department} \\%
            \@university\\%
        \end{doublespace}%
    \vspace*{\fill}%
    \begin{doublespace}
        Copyright {\copyright} {\@yearcopyrighted} {\@author}\\%
        {\@copyrighttext}%
    \end{doublespace}
    %\vspace*{\fill}%
    \par}% end centering
    }% end parindent
    \newpage
}%
%
\newcommand{\abstractpage}{%
    \clearpage
    \@@pdfbookmark[1]{Abstract}{abstract}%
    {\centering
    \parindent 0pt%
    ABSTRACT%
    \vspace{1.2\@blankline}\par
    \parbox[t]{5in}{\centering
        \@title
    \par}% end parbox
    \vspace{1.2\@blankline}\par
    {\@author}\\%
    {\@departmentprefix} {\@department}, {\@universityabbrev}\\%
    \@degreename
    \par}% end centering
    {\setlength{\parskip}{\@blankline}\par
    % parskip is applied at the beginning of paragraphs, so we add a bit of
    % length here to make it the same as above.
    \vspace{0.2\@blankline}\par
    \@documentabstract
    \par}
    \if@hasdocumentkeywords
    \vfill\par\noindent
        Keywords: \@documentkeywords
    \par
    \par
    \else
        \ClassError{byumsphd}{%
            Specification of document keywords is required.
        }%
    \fi
    \newpage
}%
%
% Create a counter for the listings that need to be referenced from the table
% of contents.  This is needed to get hyperref to link to unnumbered sections
% properly (like listoftables, etc.) without using an existing counter and
% messing up the numbering of other kinds of sections.
\newcounter{toclistings}
%
\newcommand{\acknowledgmentspage}{%
    \clearpage
    \begin{doublespace}%
    {\centering
    \parindent 0pt%
    ACKNOWLEDGMENTS%
    \vspace{2\@blankline}\par
    \par}% end centering
    \@acknowledgments
    \end{doublespace}%
    \newpage
}%
%
\renewcommand{\tableofcontents}{%
    \if@twosidetoc
        \clearpage@forchapter
    \else
        \clearpage
    \fi
    \@@pdfbookmark[1]{\contentsname}{toc}%
    \@tocheader{\contentsname}%
    \thispagestyle{plain}%
    \@starttoc{toc}%
    \newpage
}%
%
\renewcommand{\listoffigures}{%
    \if@twosidetoc
        \clearpage@forchapter
    \else
        \clearpage
    \fi
    \refstepcounter{toclistings}
    \addcontentsline{toc}{chapter}{\listfigurename}
    \@tocheader{\listfigurename}%
    \@starttoc{lof}%
    \newpage
}%
%
\renewcommand{\listoftables}{%
    \if@twosidetoc
        \clearpage@forchapter
    \else
        \clearpage
    \fi
    \refstepcounter{toclistings}
    \addcontentsline{toc}{chapter}{\listtablename}
    \@tocheader{\listtablename}%
    \@starttoc{lot}%
    \newpage
}%
%
\if@lol
\renewcommand{\lstlistlistingname}{List of Listings}
\renewcommand{\lstlistoflistings}{%
    \if@twosidetoc
        \clearpage@forchapter
    \else
        \clearpage
    \fi
    \refstepcounter{toclistings}
    \addcontentsline{toc}{chapter}{\lstlistlistingname}
    \@tocheader{\lstlistlistingname}%
    \@starttoc{lol}%
    \newpage
}%
\fi
%
\newcommand{\@separatorpage}{%
    \if@twoside
        \if@separator
            \clearpage
            \thispagestyle{empty}%
            \addtocounter{page}{-1}% Don't count this page
            {\centering
            \vspace*{\fill}
            DISCARD THIS PAGE --- IT IS ONLY A MARKER\\
            \vspace{3\@blankline}%
            All preceding pages must be single-sided.\\
            All subsequent pages must be double-sided.
            \vspace*{\fill}
            \par}% end centering
            \newpage
        \fi
    \fi
}%
%
% Lifted from report.cls and edited to be smaller
% NOTE that the minimum standards document indicates that ALL fonts should be
% 10, 11, or 12 point *including titles and headings*.  This requirement is
% incredibly ugly, but if you want to comply with it, change everything to
% normalsize in this document.
\renewcommand{\section}{\@startsection {section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\@sizelarge\bfseries}}%
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}%
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}%
%
\renewcommand{\chapter}{%
    \clearpage@forchapter
    \thispagestyle{plain}%
    \@afterindenttrue
    \global\@topnum\z@
    \secdef\@chapter\@schapter
}%
%
\newcommand{\@tocheader}[1]{%
    \begin{@headjustify}%
    \@chapterpagestyle
    \parindent 0pt%
        \begin{singlespace}%
        \vspace*{\@prefacemargingapdouble}%
        \ifnum \c@secnumdepth > \m@ne
            \@sizeLarge \bf {#1}%
            \par
            \vspace{\@blankline}%
        \fi
        \vspace{\@blankline}%
        \end{singlespace}%
        \nobreak
    \end{@headjustify}%
}%
%
%
\renewcommand{\@makechapterhead}[1]{%
    \begin{@headjustify}%
    \@chapterpagestyle
    \parindent 0pt%
        \begin{singlespace}%
        \vspace*{\@prefacemargingapdouble}%
        \ifnum \c@secnumdepth > \m@ne
            \@sizeLarge \bf
            \if@simplechapterheading
                \expandafter{%
                    \thechapter
                    \hspace{0.25in}%
                    \MakeUppercase{#1}%
                }%
            \else
                \expandafter{\@chapapp{} \thechapter}%
            \fi
            \par
            \vspace{\@blankline}%
        \fi
        \end{singlespace}%
        \if@simplechapterheading\else
            \@sizelarge \bf {#1} \par
        \fi
        \begin{singlespace}%
        \vspace{\@blankline}%
        \end{singlespace}%
        \nobreak
    \end{@headjustify}%
}%
%
\renewcommand{\@makeschapterhead}[1]{%
    \begin{@headjustify}
    \@chapterpagestyle
    \parindent 0pt%
        \begin{singlespace}%
        \vspace*{\@prefacemargingapdouble}%
        \@sizelarge \bf {#1} \par
        \vspace{\@blankline}%
        \end{singlespace}%
        \nobreak
    \end{@headjustify}%
}%
%
\renewcommand{\part}{%
    \clearpage@forchapter
    \@chapterpagestyle
    \@parttopspace
    \secdef\@part\@spart
}%
%
\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >-2\relax
        \refstepcounter{part}%
        \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
    \else
        \addcontentsline{toc}{part}{#1}%
    \fi
    \markboth{}{}% empty headings
    {\centering
        \interlinepenalty \@M
        \normalfont
        \ifnum \c@secnumdepth >-2\relax
            \@sizehuge\bfseries \partname\nobreakspace\thepart
            \par
            \vskip 20\p@
        \fi
        \@sizeHuge \bfseries #2%
    \par}% end centering
    \@partbottomspace
}%
%
\def\@spart#1{%
    \addcontentsline{toc}{part}{#1}%
    \@chapterpagestyle
    {\centering
        \interlinepenalty \@M
        \normalfont
        \@sizeHuge \bfseries #1%
    \par}% end centering
    \@partbottomspace
}%
%
\let\old@bibliography\bibliography
\renewcommand{\bibliography}[1]{%
    \onehalfspace\par
    \old@bibliography{#1}%
}%
%
\renewcommand{\maketitle}{%
    \begin{singlespace}%
    \pagenumbering{roman}%
    {%
        \pagestyle{empty}%
        % The front matter is one-sided, so the margins don't alternate
        \if@equalmargins\else
            \addtolength{\evensidemargin}{\@bindingoffset}%
        \fi
        \titlepage
        \abstractpage
        \if@hasacknowledgments
            \acknowledgmentspage
        \fi
    }%
    {%
        \if@twosidetoc
            % If we are beginning two-sided at the TOC, then the separator page
            % belongs here (if anywhere).
            \@separatorpage
        \else
            % Otherwise, we need to make our margins one-sided again in this
            % block.
            \if@equalmargins\else
                \addtolength{\evensidemargin}{\@bindingoffset}%
            \fi
        \fi
        \pagestyle{plain}%
        \begin{doublespace}%
            \tableofcontents
            \if@lof
                \listoffigures
            \fi
            \if@lot
                \listoftables
            \fi
            \if@lol
                \lstlistoflistings
            \fi
            \if@twosidetoc\else
                % If we start two-sided printing after the various tables (body
                % only), then we print the separator here.
                \@separatorpage
            \fi
        \end{doublespace}%
    }%
    \end{singlespace}%
    \if@duplexprinter
        \@clearemptydoublepage
    \fi
    % Body starts here
    \clearpage@forchapter
    \pagenumbering{arabic}%
}%
%
% Different font in captions
\newcommand{\captionfonts}{\small}
%
% Fix the abstract environment for individual chapters
\renewenvironment{abstract}%
{%
    \begin{singlespace}%
    {\vspace*{\fill}\centering\bf\@sizelarge Abstract\bigskip\par}%
    \end{singlespace}%
    \begingroup\noindent
}%
{%
    \endgroup\vspace*{\fill}%
}%
%
%
% Set up default document settings
\AtBeginDocument{%
    \pagestyle{plain}%
    \pagenumbering{arabic}%
    \parindent \@defaultindent
    % Fix the bibliography stuff (if using natbib).
    \@ifpackageloaded{natbib}{% natbib loaded
        \renewcommand{\bibname}{\refname}
        \let\oldbibsection\bibsection
        \renewcommand{\bibsection}{%
            \oldbibsection
            \refstepcounter{toclistings}%
            \addcontentsline{toc}{chapter}{\refname}
        }%
    }{% natbib not loaded
        \ClassWarning{byumsphd}{Not using natbib - TOC might not show references.  Search class file comments for "NATBIB" for how to resolve this by hand (or just use natbib - it's an excellent package)}
        \renewcommand{\bibname}{References}
    }%
    % Set up double spacing---this is safe because the overall document is
    % single-spaced and we'll set up single spacing as the default in maketitle
    % where spacing matters.
    \doublespace
}%
%
\newcommand{\@subtitle}{}
% vim: ft=tex sw=4 sts=4
