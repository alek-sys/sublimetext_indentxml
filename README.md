# SublimeText Indent plugin

<p>What is the goal of Indent plugin? Short answer is converting this XML</p>
    <root><node attr="1" attr2="4"><node /></node></root>
<p>to this: </p>
    <root>
        <node attr="1" attr2="4">
		    <node/>
	    </node>
    </root>

<p>Looks good? It also can convert this JSON</p>
    { "root": [ { "field": "val1", "field2": "val2" }, { "arr": [1, 3, "three"] }] }
<p>to this</p>
    {
        "root": [
            {
                "field": "val1",
                "field2": "val2"
            },
            {
                "arr": [
                    1,
                    3,
                    "three"
                ]
            }
        ]
    }
    
<p>Want more? It can indent only selected text - including multiple selections and even mixed XML / JSON selections. It is smart enough to recognize XML or JSON even if you are editing plain text. Indent plugin won't mess up your keyboard shortcuts because it uses "chord" command Ctrl+K, Ctrl+F (this mean hold Ctrl, press K then press F, release Ctrl) and also available in "Selection" menu. </p>

## Supported Sublime Text versions
Indent plugin supports both Sublime Text 2 and Sublime Text 3

## Installation
In Sublime Text 2 - just use [Package Control](http://wbond.net/sublime_packages/package_control) and search for "indentxml" plugin
In Sublime Text 3 - clone project from [Github](https://github.com/alek-sys/sublimetext_indentxml.git) into Packages folder.

## Feedback & Support
Available on [Github](https://github.com/alek-sys/sublimetext_indentxml)

## Contribution
...is always welcome! Same place - [Github](https://github.com/alek-sys/sublimetext_indentxml)

## License
This software is distributed under MIT license (see License.txt for details)