SQLRunner
=========

SqlRunner enables sending the selected region in Sublime Text to a command- line
SQL client. Results are then put into a scratch file. By tying into the existing
client, this allows the use of informational commands (such as `\d` in `psql`)
to pull data that's not typically available via straight SQL.

Settings
========

I realize that working on a few different projects may well wind up with you needing to connecting to different types and instances of databases on a per-project basis, so SQLRunner supports completely duplicating its settings in your project file as well as under Preferences.

SQLRunner respects settings in the global defaults (`SQLRunner.sublime-settings`) as well as local project settings. It will first look in the per-project settings under the key `SQLRunner`, before moving on to the defaults. For example, in your project file:

```json
{
	"folders":
	[
		{
			"path": "/Users/matt/Library/Application Support/Sublime Text 2/Packages/SQLRunner"
		}
	],
	"settings": {
		"SQLRunner": {
			"display_type": "file"
		},
		"tab_size": 18,
	},
	"build_systems":
	[
	    {
	    	"name": "List",
	    	"cmd": ["ls"]
	    }
	]
}
```

General
-------

The following settings are general to operation and don't have any reliance on any specific database.

* `display_type`: "file" or "console", for either opening up a scratch file or display 

Contributions
=============
Borrows output display code from [SublimeText-NodeEval](https://github.com/mediaupstream/SublimeText-NodeEval)

License
=======
All of SQLRunner is licensed under the MIT license.

Copyright (c) 2013 Matthew Erickson <peawee@peawee.net>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.