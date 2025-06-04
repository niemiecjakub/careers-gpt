from data.vanna import vn

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
plan = vn.get_training_plan_generic(df_information_schema)
vn.train(plan=plan)

vn.train(
    ddl="""
    CREATE TABLE public.company (
        id serial4 NOT NULL,
        name varchar NOT NULL,
        embedding public.vector NULL,
        CONSTRAINT company_name_key UNIQUE (name),
        CONSTRAINT company_pkey PRIMARY KEY (id)
    );
    """
)

vn.train(
    ddl="""
    CREATE TABLE public.employment_duration (
        id serial4 NOT NULL,
        duration varchar NOT NULL,
        CONSTRAINT employment_duration_duration_key UNIQUE (duration),
        CONSTRAINT employment_duration_pkey PRIMARY KEY (id)
    );
    """
)

vn.train(
    ddl="""
    CREATE TABLE public.employment_status (
        id serial4 NOT NULL,
        status varchar NOT NULL,
        is_current bool NOT NULL,
        CONSTRAINT employment_status_pkey PRIMARY KEY (id),
        CONSTRAINT employment_status_status_key UNIQUE (status)
    );
    """
)

vn.train(
    ddl="""
    CREATE TABLE public.opinion (
        id serial4 NOT NULL,
        symbol varchar NOT NULL,
        opinion varchar NOT NULL,
        CONSTRAINT opinion_opinion_key UNIQUE (opinion),
        CONSTRAINT opinion_pkey PRIMARY KEY (id),
        CONSTRAINT opinion_symbol_key UNIQUE (symbol)
    );
    """
)

vn.train(
    ddl="""
    CREATE TABLE public.review (
        id serial4 NOT NULL,
        rating int4 NULL,
        review_title text NULL,
        employment_status_id int4 NULL,
        employment_duration_id int4 NULL,
        pros text NULL,
        cons text NULL,
        recommended bool NULL,
        ceo_opinion_id int4 NULL,
        business_outlook_opinion_id int4 NULL,
        career_opportunities int4 NULL,
        compensation_and_benefits int4 NULL,
        senior_management int4 NULL,
        work_life_balance int4 NULL,
        culture_and_values int4 NULL,
        diversity_and_inclusion int4 NULL,
        company_id int4 NOT NULL,
        date date NULL,
        job_title text NULL,
        embedding public.vector NULL,
        CONSTRAINT review_pkey PRIMARY KEY (id)
    );
    """
)

vn.train(
    ddl="""
    CREATE TABLE public.company (
        id serial4 NOT NULL,
        name varchar NOT NULL,
        embedding public.vector NULL,
        CONSTRAINT company_name_key UNIQUE (name),
        CONSTRAINT company_pkey PRIMARY KEY (id)
    );

    CREATE TABLE public.employment_duration (
        id serial4 NOT NULL,
        duration varchar NOT NULL,
        CONSTRAINT employment_duration_duration_key UNIQUE (duration),
        CONSTRAINT employment_duration_pkey PRIMARY KEY (id)
    );

    CREATE TABLE public.employment_status (
        id serial4 NOT NULL,
        status varchar NOT NULL,
        is_current bool NOT NULL,
        CONSTRAINT employment_status_pkey PRIMARY KEY (id),
        CONSTRAINT employment_status_status_key UNIQUE (status)
    );

    CREATE TABLE public.opinion (
        id serial4 NOT NULL,
        symbol varchar NOT NULL,
        opinion varchar NOT NULL,
        CONSTRAINT opinion_opinion_key UNIQUE (opinion),
        CONSTRAINT opinion_pkey PRIMARY KEY (id),
        CONSTRAINT opinion_symbol_key UNIQUE (symbol)
    );

    CREATE TABLE public.review (
        id serial4 NOT NULL,
        rating int4 NULL,
        review_title text NULL,
        employment_status_id int4 NULL,
        employment_duration_id int4 NULL,
        pros text NULL,
        cons text NULL,
        recommended bool NULL,
        ceo_opinion_id int4 NULL,
        business_outlook_opinion_id int4 NULL,
        career_opportunities int4 NULL,
        compensation_and_benefits int4 NULL,
        senior_management int4 NULL,
        work_life_balance int4 NULL,
        culture_and_values int4 NULL,
        diversity_and_inclusion int4 NULL,
        company_id int4 NOT NULL,
        date date NULL,
        job_title text NULL,
        embedding public.vector NULL,
        CONSTRAINT review_pkey PRIMARY KEY (id)
    );
    """
)

vn.train(
    ddl="""
    CREATE TABLE public.company (
        id serial4 NOT NULL,
        name varchar NOT NULL,
        embedding public.vector NULL,
        CONSTRAINT company_name_key UNIQUE (name),
        CONSTRAINT company_pkey PRIMARY KEY (id)
    );

    CREATE TABLE public.employment_duration (
        id serial4 NOT NULL,
        duration varchar NOT NULL,
        CONSTRAINT employment_duration_duration_key UNIQUE (duration),
        CONSTRAINT employment_duration_pkey PRIMARY KEY (id)
    );

    CREATE TABLE public.employment_status (
        id serial4 NOT NULL,
        status varchar NOT NULL,
        is_current bool NOT NULL,
        CONSTRAINT employment_status_pkey PRIMARY KEY (id),
        CONSTRAINT employment_status_status_key UNIQUE (status)
    );

    CREATE TABLE public.opinion (
        id serial4 NOT NULL,
        symbol varchar NOT NULL,
        opinion varchar NOT NULL,
        CONSTRAINT opinion_opinion_key UNIQUE (opinion),
        CONSTRAINT opinion_pkey PRIMARY KEY (id),
        CONSTRAINT opinion_symbol_key UNIQUE (symbol)
    );

    CREATE TABLE public.review (
        id serial4 NOT NULL,
        rating int4 NULL,
        review_title text NULL,
        employment_status_id int4 NULL,
        employment_duration_id int4 NULL,
        pros text NULL,
        cons text NULL,
        recommended bool NULL,
        ceo_opinion_id int4 NULL,
        business_outlook_opinion_id int4 NULL,
        career_opportunities int4 NULL,
        compensation_and_benefits int4 NULL,
        senior_management int4 NULL,
        work_life_balance int4 NULL,
        culture_and_values int4 NULL,
        diversity_and_inclusion int4 NULL,
        company_id int4 NOT NULL,
        date date NULL,
        job_title text NULL,
        embedding public.vector NULL,
        CONSTRAINT review_pkey PRIMARY KEY (id)
    );
    """
)

questions_sql = [
    {
        "question": "What companies have the highest average rating?",
        "sql": """
            SELECT 
                c.name, 
                AVG(r.rating) AS avg_rating,
                COUNT(*) AS review_count
            FROM review r
            JOIN company c ON r.company_id = c.id
            GROUP BY c.name
            HAVING COUNT(*) > 10000
            ORDER BY avg_rating desc
            LIMIT 100;
        """
    },
    {
        "question": "Which companies have the most recommendations by employees?",
        "sql": """
            SELECT c.name, COUNT(*) AS recommended_count
            FROM review r
            JOIN company c ON r.company_id = c.id
            WHERE r.recommended = true
            GROUP BY c.name
            ORDER BY recommended_count DESC
            LIMIT 100;
        """
    },
    {
        "question": "Which companies have the highest average ratings for work-life balance, compensation, and senior management?",
        "sql": """
            SELECT c.name, 
                AVG(r.work_life_balance) AS avg_wlb,
                AVG(r.compensation_and_benefits) AS avg_comp,
                AVG(r.senior_management) AS avg_mgmt
            FROM review r
            JOIN company c ON r.company_id = c.id
            GROUP BY c.name
            HAVING COUNT(*) >= 5000
               AND AVG(r.work_life_balance) IS NOT NULL 
               AND AVG(r.compensation_and_benefits) IS NOT NULL 
               AND AVG(r.senior_management) IS NOT NULL
            ORDER BY avg_wlb DESC, avg_comp DESC, avg_mgmt DESC
            LIMIT 100;
        """
    },
    {
        "question": "What are the most common pros and cons mentioned for Amazon?",
        "sql": """
            SELECT r.pros, r.cons
            FROM review r
            JOIN company c ON r.company_id = c.id
            WHERE c.name = 'Amazon'
            LIMIT 100;
        """
    },
    {
        "question": "What is the typical employment duration for Amazon?",
        "sql": """
            SELECT ed.duration, COUNT(*) AS count
            FROM review r
            JOIN company c ON r.company_id = c.id
            JOIN employment_duration ed ON r.employment_duration_id = ed.id
            WHERE c.name = 'Amazon'
            GROUP BY ed.duration
            ORDER BY count DESC;
        """
    },
    {
        "question": "What employment statuses do reviewers usually have?",
        "sql": """
            SELECT 
                es.is_current, 
                COUNT(*) AS count
            FROM review r
            JOIN employment_status es ON r.employment_status_id = es.id
            GROUP BY es.is_current
            ORDER BY count DESC;
        """
    },
    {
        "question": "What is the sentiment for business outlook for Google?",
        "sql": """
            SELECT 
                c.name,
                o.opinion AS business_outlook_opinion,
                COUNT(*) AS opinion_count
            FROM review r
            JOIN company c ON r.company_id = c.id
            LEFT JOIN opinion o ON r.business_outlook_opinion_id = o.id
            WHERE c.name = 'Google'
            GROUP BY c.name, o.opinion
            ORDER BY opinion_count DESC;
        """
    },
    {
        "question": "Compare IBM and Infosys in terms of rating, work-life balance, compensation, and culture.",
        "sql": """
            SELECT c.name,
                   AVG(r.rating) AS avg_rating,
                   AVG(r.work_life_balance) AS avg_wlb,
                   AVG(r.compensation_and_benefits) AS avg_comp,
                   AVG(r.senior_management) AS avg_mgmt,
                   AVG(r.culture_and_values) AS avg_culture
            FROM review r
            JOIN company c ON r.company_id = c.id
            WHERE c.name IN ('IBM', 'Infosys')
            GROUP BY c.name;
        """
    },
    {
        "question": "Which companies have the worst ratio of recommended to not recommended reviews?",
        "sql": """
            SELECT 
                c.name,
                COUNT(*) FILTER (WHERE r.recommended = true) AS recommended_count,
                COUNT(*) FILTER (WHERE r.recommended = false) AS not_recommended_count,
                COUNT(*) AS total_reviews,
                (COUNT(*) FILTER (WHERE r.recommended = true)::float / NULLIF(COUNT(*) FILTER (WHERE r.recommended = false), 0)) AS recommended_to_not_recommended_ratio
            FROM review r
            JOIN company c ON r.company_id = c.id
            GROUP BY c.name
            HAVING COUNT(*) >= 8000
            ORDER BY recommended_to_not_recommended_ratio ASC NULLS LAST
            LIMIT 100;
        """
    },  
        {
        "question": "Which companies have the worst ratio of recommended to not recommended reviews among current employees?",
        "sql": """
            SELECT 
                c.name,
                COUNT(*) FILTER (WHERE r.recommended = true) AS recommended_count,
                COUNT(*) FILTER (WHERE r.recommended = false) AS not_recommended_count,
                COUNT(*) AS total_reviews,
                (COUNT(*) FILTER (WHERE r.recommended = true)::float / NULLIF(COUNT(*) FILTER (WHERE r.recommended = false), 0)) AS recommended_to_not_recommended_ratio
            FROM review r
            JOIN company c ON r.company_id = c.id
            JOIN employment_status es ON r.employment_status_id = es.id
            WHERE es.is_current = true
            GROUP BY c.name
            HAVING COUNT(*) >= 5000
            ORDER BY recommended_to_not_recommended_ratio ASC NULLS LAST
            LIMIT 100; 
        """
    },  
    {
        "question": "Which companies have the lowest average ratings for diversity and inclusion?",
        "sql": """
            SELECT c.name, AVG(r.diversity_and_inclusion) AS avg_diversity
            FROM review r
            JOIN company c ON r.company_id = c.id
            GROUP BY c.name
            HAVING COUNT(*) > 5000
            ORDER BY avg_diversity ASC  
            LIMIT 100;
        """
    },
    {
        "question": "Find companies with positive business outlook and high career opportunity ratings.",
        "sql": """
            SELECT 
                c.name, 
                AVG(r.career_opportunities) AS avg_career_opp
            FROM review r
            JOIN company c ON r.company_id = c.id
            JOIN opinion o ON r.business_outlook_opinion_id = o.id
            WHERE o.opinion  = 'Positive'
            GROUP BY c.name
            HAVING AVG(r.career_opportunities) >= 4
            AND COUNT(*) > 5000
            ORDER BY avg_career_opp DESC;
            LIMIT 100;
        """
    },
    {
        "question": "What job titles are most common among reviewers at IBM?",
        "sql": """
            SELECT r.job_title, COUNT(*) AS count
            FROM review r
            JOIN company c ON r.company_id = c.id
            WHERE c.name = 'IBM'
            GROUP BY r.job_title
            ORDER BY count DESC
            LIMIT 100;
        """
    },
    {
        "question": "Which jobs report highest work-life balance or lowest compensation dissatisfaction?",
        "sql": """
            SELECT 
                r.job_title,
                AVG(r.work_life_balance) AS avg_wlb,
                AVG(r.compensation_and_benefits) AS avg_comp
            FROM review r
            GROUP BY r.job_title
            HAVING COUNT(*) >= 5000
               AND AVG(r.work_life_balance) IS NOT NULL
               AND AVG(r.compensation_and_benefits) IS NOT NULL
            ORDER BY avg_wlb DESC, avg_comp DESC
            LIMIT 100;
        """
    },
    {
        "question": "How does business outlook sentiment differ between current and former employees at Microsoft?",
        "sql": """
            SELECT es.is_current, o.opinion, COUNT(*) AS count
            FROM review r
            JOIN company c ON r.company_id = c.id
            JOIN employment_status es ON r.employment_status_id = es.id
            JOIN opinion o ON r.business_outlook_opinion_id = o.id
            WHERE c.name = 'Microsoft'
            GROUP BY es.is_current, o.opinion
            ORDER BY es.is_current DESC, count DESC;
        """
    },
    {
        "question": "Which job titles most frequently recommend their employer?",
        "sql": """
            SELECT r.job_title, COUNT(*) FILTER (WHERE r.recommended = true)::float / COUNT(*) AS recommendation_rate
            FROM review r
            WHERE r.job_title IS NOT NULL
            GROUP BY r.job_title
            HAVING COUNT(*) >= 5000
            ORDER BY recommendation_rate DESC
            LIMIT 30;
        """
    },
    {
        "question": "Which companies have the highest variance in overall ratings?",
        "sql": """
            SELECT c.name, STDDEV(r.rating) AS rating_stddev
            FROM review r
            JOIN company c ON r.company_id = c.id
            GROUP BY c.name
            HAVING COUNT(*) >= 5000
            ORDER BY rating_stddev DESC
            LIMIT 100;
        """
    },
    {
        "question": "Which companies have the lowest compensation satisfaction among current employees?",
        "sql": """
            SELECT c.name, AVG(r.compensation_and_benefits) AS avg_comp
            FROM review r
            JOIN company c ON r.company_id = c.id
            JOIN employment_status es ON r.employment_status_id = es.id
            WHERE es.is_current = true
            GROUP BY c.name
            HAVING COUNT(*) > 5000
            ORDER BY avg_comp ASC
            LIMIT 100;
        """
    },
    {
        "question": "What is the average recommendation rate for different employment durations across all companies?",
        "sql": """
            SELECT
                ed.duration,
                (COUNT(*) FILTER (WHERE r.recommended = true) * 100.0 / COUNT(*)) AS recommendation_percentage
            FROM review r
            JOIN employment_duration ed ON r.employment_duration_id = ed.id
            WHERE r.recommended IS NOT NULL
            GROUP BY ed.duration
        """
    },
]

i = 1
for item in questions_sql:
    print(f"Training {i}/{len(questions_sql)}")
    vn.train(question=item["question"], sql=item["sql"])
    i+= 1