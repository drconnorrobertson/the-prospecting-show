"""Check a local editorial quote ledger. Exact text matching is not fact checking or rights clearance."""
import argparse
import csv
import json

FIELDS=['note_id','episode_id','speaker','locator','kind','source_excerpt','draft_text','approval']

def check(path):
    issues=[];seen=set();count=0
    with open(path,encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream,strict=True)
        if reader.fieldnames!=FIELDS:raise ValueError('headers must be exactly: '+','.join(FIELDS))
        for n,raw in enumerate(reader,2):
            count+=1
            if None in raw or any(v is None for v in raw.values()):raise ValueError('wrong number of fields at record '+str(n))
            row={k:v.strip() for k,v in raw.items()};codes=[]
            if not row['note_id']:codes.append('missing_id')
            elif row['note_id'] in seen:codes.append('duplicate_id')
            seen.add(row['note_id'])
            for field in ('episode_id','speaker','locator','draft_text'):
                if not row[field]:codes.append('missing_'+field)
            if row['kind'] not in ('verbatim','paraphrase','editorial_idea'):codes.append('invalid_kind')
            if row['kind'] in ('verbatim','paraphrase') and not row['source_excerpt']:codes.append('missing_source_excerpt')
            if row['kind']=='verbatim' and row['draft_text']!=row['source_excerpt']:codes.append('verbatim_mismatch')
            if row['kind']=='paraphrase' and row['draft_text'].startswith(('"','“')):codes.append('paraphrase_starts_with_quote')
            if row['approval']!='approved':codes.append('not_approved')
            if codes:issues.append({'record':n,'note_id':row['note_id'],'issues':codes})
    if count==0:raise ValueError('no data records')
    return {'records':count,'flagged_records':len(issues),'issues':issues,'fact_check_or_rights_clearance':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv_file');args=p.parse_args()
    try:result=check(args.csv_file)
    except (ValueError,OSError,csv.Error) as error:p.exit(2,'Input error: '+str(error)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
