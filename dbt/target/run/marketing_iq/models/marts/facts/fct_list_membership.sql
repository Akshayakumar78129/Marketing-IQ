-- back compat for old kwarg name
  
  begin;
    
        
            
	    
	    
            
        
    

    

    merge into CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_list_membership as DBT_INTERNAL_DEST
        using CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_list_membership__dbt_tmp as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.list_membership_sk = DBT_INTERNAL_DEST.list_membership_sk))

    
    when matched then update set
        "LIST_MEMBERSHIP_SK" = DBT_INTERNAL_SOURCE."LIST_MEMBERSHIP_SK","PLATFORM" = DBT_INTERNAL_SOURCE."PLATFORM","LIST_ID" = DBT_INTERNAL_SOURCE."LIST_ID","PERSON_ID" = DBT_INTERNAL_SOURCE."PERSON_ID","JOINED_AT" = DBT_INTERNAL_SOURCE."JOINED_AT","JOINED_DATE" = DBT_INTERNAL_SOURCE."JOINED_DATE","IS_ACTIVE_MEMBER" = DBT_INTERNAL_SOURCE."IS_ACTIVE_MEMBER","LAST_SYNCED" = DBT_INTERNAL_SOURCE."LAST_SYNCED"
    

    when not matched then insert
        ("LIST_MEMBERSHIP_SK", "PLATFORM", "LIST_ID", "PERSON_ID", "JOINED_AT", "JOINED_DATE", "IS_ACTIVE_MEMBER", "LAST_SYNCED")
    values
        ("LIST_MEMBERSHIP_SK", "PLATFORM", "LIST_ID", "PERSON_ID", "JOINED_AT", "JOINED_DATE", "IS_ACTIVE_MEMBER", "LAST_SYNCED")

;
    commit;