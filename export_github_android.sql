SELECT type, created_at, repository_owner, repository_name, 
       actor_attributes_email, actor_attributes_login, actor_attributes_name
FROM [githubarchive:github.timeline]
WHERE repository_name="android" AND
    type != "WatchEvent" AND
    repository_owner IN (
      SELECT actor_attributes_login
      FROM [githubarchive:github.timeline]
      WHERE repository_name="android" AND
            repository_owner="github" AND
            type!="WatchEvent"
    )
ORDER BY created_at
;

