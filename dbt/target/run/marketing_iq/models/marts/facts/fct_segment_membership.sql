-- back compat for old kwarg name
  
  begin;
    
        
            
	    
	    
            
        
    

    

    merge into CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_segment_membership as DBT_INTERNAL_DEST
        using CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_segment_membership__dbt_tmp as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.segment_membership_sk = DBT_INTERNAL_DEST.segment_membership_sk))

    
    when matched then update set
        "SEGMENT_MEMBERSHIP_SK" = DBT_INTERNAL_SOURCE."SEGMENT_MEMBERSHIP_SK","PLATFORM" = DBT_INTERNAL_SOURCE."PLATFORM","SEGMENT_ID" = DBT_INTERNAL_SOURCE."SEGMENT_ID","PERSON_ID" = DBT_INTERNAL_SOURCE."PERSON_ID","IS_ACTIVE_MEMBER" = DBT_INTERNAL_SOURCE."IS_ACTIVE_MEMBER","MEMBERSHIP_TIMESTAMP" = DBT_INTERNAL_SOURCE."MEMBERSHIP_TIMESTAMP","MEMBERSHIP_DATE" = DBT_INTERNAL_SOURCE."MEMBERSHIP_DATE"
    

    when not matched then insert
        ("SEGMENT_MEMBERSHIP_SK", "PLATFORM", "SEGMENT_ID", "PERSON_ID", "IS_ACTIVE_MEMBER", "MEMBERSHIP_TIMESTAMP", "MEMBERSHIP_DATE")
    values
        ("SEGMENT_MEMBERSHIP_SK", "PLATFORM", "SEGMENT_ID", "PERSON_ID", "IS_ACTIVE_MEMBER", "MEMBERSHIP_TIMESTAMP", "MEMBERSHIP_DATE")

;
    commit;