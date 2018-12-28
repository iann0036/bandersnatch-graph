import json
import pprint
import urllib.request
import os

with open('jsonGraph.json') as f:
    raw_data = json.load(f)

choice_points = raw_data['jsonGraph']['videos']['80988062']['interactiveVideoMoments']['value']['choicePointNavigatorMetadata']['choicePointsMetadata']['choicePoints']
moments_by_segment = raw_data['jsonGraph']['videos']['80988062']['interactiveVideoMoments']['value']['momentsBySegment']

pprint.pprint(choice_points)
pprint.pprint(moments_by_segment)

dot_output = "digraph bandersnatch {\n\
    node [shape=plaintext]\n\
    \n\
"

for cp_key, cp in choice_points.items():
    if 'image' in cp:
        url = cp['image']['styles']['backgroundImage'][4:-1]
        
        urllib.request.urlretrieve(url, "%s.webp" % cp_key)
        os.system('/usr/local/bin/convert %s.webp %s.png' % (cp_key, cp_key))

    dot_output += "    NODE%s [label=<<TABLE><TR><TD><IMG SRC=\"%s.png\"/></TD></TR><TR><TD>%s</TD></TR></TABLE>>, fillcolor=white, style=filled];\n" % (cp_key.replace("-",""), cp_key, cp['description'])
    pprint.pprint(cp)

dot_output += "\n"
for mbs_key, mbs in moments_by_segment.items():
    for moment in mbs:
        if 'choices' in moment:
            for choice in moment['choices']:
                sid = choice['id']
                if 'segmentId' in choice:
                    sid = choice['segmentId']

                if 'text' in choice:
                    dot_output += "    NODE%s -> NODE%s [label=\"%s\"]\n" % (mbs_key.replace("-",""), sid.replace("-",""), choice['text'])
                else:
                    dot_output += "    NODE%s -> NODE%s\n" % (mbs_key.replace("-",""), sid.replace("-",""))

dot_output += "\n}"

with open('output.dot', 'w') as f:
    f.write(dot_output)

os.system('/usr/local/bin/dot -Tpng output.dot -o output.png')