defaultFsgram= """
Pessoa : H* , Bio, Foto.
Album : Foto*.

H : r'h[0-9]+\-\w+\.\w+'
Bio : r'b[0-9]+\-\w+\.\w+'
Foto : r'p[0-9]+\-\w+\.\w+'

UNIVERSE

Story -> title,author,date
Biography -> name,birthday,birthplace,occupation,death
Foto -> note,date

IGNORE
.py 
.out
.fsgram
"""

frontdgubook = r"""
\documentclass[12pt]{article}
\usepackage{geometry}
\geometry{letterpaper, margin=1in}

\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{titlesec}

\titleformat*{\section}{\huge\bfseries\color{blue}}
\titleformat*{\subsection}{\LARGE\bfseries\color{orange}}

\title{Auto-Generated Stories}
\author{}
\date{\vspace{-5ex}}

\begin{document}

\maketitle

\section*{Introduction}

Welcome to this collection of auto-generated stories! These tales were created using advanced algorithms and artificial intelligence techniques, and are sure to delight and intrigue readers of all ages.
"""

markdownbook= """# Ancestors Notebook

<sup>*Automatically generated*</sup>

## Table of Contents"""









templateLatex = r"""
\documentclass{article}

\usepackage{subcaption}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{tcolorbox}
\usepackage{calc}
\usepackage{chronology}
\usepackage{geometry}

\geometry{
    a4paper,
    total={170mm,257mm},
    left=20mm,
    top=20mm,
}
\newlength{\mytopmargin}
\setlength{\mytopmargin}{\oddsidemargin}
\addtolength{\mytopmargin}{\topmargin}
\addtolength{\mytopmargin}{1in}
\geometry{top=\mytopmargin+0.5in}


\title{ {{tit}} }
\author{ {{autor}} }
\date{ {{-day-}} }

\begin{document}

\maketitle
\tableofcontents

\newpage
\newcounter{tablecounter}

{% for h in hs %}
\newpage

\begin{center}
\section{ {{-h.title-}} }
\vspace{0.5cm}
{% if h.author is defined and h.author != 'False' %}
    {% if h.author|length > 1 %}
        \textit{by}
        {% for a in h.author[:-1] %}
            {{ a }},
        {% endfor %}
        {{ h.author[-1] }}
    {% else %}
        \textit{by} {{h.author[0]}}
    {% endif %}
{% endif %}
\vspace{0.75cm}
{% if h.about is defined and h.about|length > 0 %} 
    \fbox{
        \begin{minipage}{0.9\textwidth}
            \vspace{0.2cm}
            \textbf{\textit{About}}
            \begin{itemize}
                {% for about in h.about %}
                    \item \textit{ {{about}} }
                {% endfor %}
            \end{itemize}
            \vspace{0.2cm}
        \end{minipage}
    }
    {% endif %}
\vspace{0.75cm}
    $\ast$~$\ast$~$\ast$  


    \begin{center}
        \begin{minipage}{0.9\textwidth}
            \setlength{\parskip}{0.2cm}
            \setlength{\parindent}{0cm}
            \fontsize{12pt}{14pt}\selectfont
            {{h.corpo}}
        \end{minipage}
    \end{center}
\end{center}
    \stepcounter{tablecounter}
    {% if h|length > 3 %}
        \textsuperscript{\hyperref[table:\arabic{tablecounter}]{See metadata here}}
    {% endif %}

{% endfor %}

\clearpage
\section{Images}

\newcounter{image}

{% for img in imgs %}

    \begin{figure}[ht!]
    \begin{minipage}{0.35\textwidth}
        \centering
        \includegraphics[width=\linewidth]{ {{-img.path-}} }
        \caption{ {{img.id}} }
    \end{minipage}
    \hspace{1cm} % add some horizontal space here
    \begin{minipage}{0.3\textwidth}
        \begin{tcolorbox}[colback=white, colframe=black, boxrule=1pt]
            \begin{itemize}
                \item {{img.format}}
                \item {{img.about}}
            \end{itemize}

        \end{tcolorbox}
    \end{minipage}
\end{figure}

{% endfor %}

\clearpage
\section{Meta-information}
\newcounter{tablecounter2}

{% for h in hs %}
    \stepcounter{tablecounter2}
    \begin{table}[ht!]
        \centering
        \begin{tabular}{|c|c|}
            \hline
            {% for k, v in h.items() if k not in ['title', 'author', 'corpo', 'about','path'] %}
                \textbf{ {{ k }} } & \textit{ {{ v }} } \\
                \hline
            {% endfor %}
        \end{tabular}
        \caption{A \textbf{ {{h.type}} }-\textit{ {{h.id}} }} % Add a caption to the table with the current table counter value
        \label{table:\arabic{tablecounter2}} % Use the current table counter value as the label name
    \end{table}
{% endfor %}

\clearpage
\section{Time Frame}

\begin{chronology}[10]{1900}{2023}{\textwidth}

{% for d in dates %}
    \event{ {{-d.date-}}  }{ {{-d.id-}} }
{% endfor %}
\end{chronology}

\end{document}
"""













templateHtml = """
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>{{tit}}</title>
	<style>
		body {
			font-family: Arial, sans-serif;
		}
		h1 {
			text-align: center;
		}
		h2 {
			margin-top: 2em;
		}
		section {
			margin: 2em 0;
		}
		img {
			max-width: 100%;
		}
		figure {
			display: flex;
			flex-direction: row;
			align-items: center;
			margin-bottom: 2em;
		}
		figcaption {
			margin-left: 1em;
			font-size: 0.8em;
			font-style: italic;
		}
		table {
			border-collapse: collapse;
			width: 100%;
			margin-top: 2em;
		}
		th, td {
			border: 1px solid black;
			padding: 0.5em;
			text-align: left;
			vertical-align: top;
		}
		th {
			background-color: #ccc;
		}
	</style>
</head>
<body>
	<h1>{{tit}}</h1>

	{% for h in hs %}
	<section>
		<h2>{{h.title}}</h2>
		{% if h.author is defined and h.author != 'False' %}
			{% if h.author|length > 1 %}
				<p><em>by
				{% for a in h.author[:-1] %}
					{{ a }},
				{% endfor %}
				{{ h.author[-1] }}</em></p>
			{% else %}
				<p><em>by {{h.author[0]}}</em></p>
			{% endif %}
		{% endif %}
		{% if h.about is defined and h.about|length > 0 %}
			<div>
				<h3>About</h3>
				<ul>
				{% for about in h.about %}
					<li><em>{{about}}</em></li>
				{% endfor %}
				</ul>
			</div>
		{% endif %}
		<div>{{h.corpo}}</div>
		{% if h|length > 3 %}
			<p><sup><a href="#metadata{{loop.index}}">See metadata here</a></sup></p>
		{% endif %}
	</section>
	{% endfor %}

	<section>
		<h2>Images</h2>
		{% for img in imgs %}
		<figure>
			<img src="{{img.path}}" alt="{{img.id}}">
			<figcaption>
				<p>{{img.about}}</p>
				<p>{{img.format}}</p>
			</figcaption>
		</figure>
		{% endfor %}
	</section>

	<section>
		<h2>Meta-information</h2>
		{% for h in hs %}
		<table id="metadata{{loop.index}}">
			{% for k, v in h.items() if k not in ['title', 'author', 'corpo', 'about','path'] %}
			<tr>
				<th>{{k}}</th>
				<td>{{v}}</td>
			</tr>
			{% endfor %}
		</table>
		{% endfor %}
	</section>
</body>
</html>
"""