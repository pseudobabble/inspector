import itertools

import torch
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")

# Two lists of sentences
queries = """
five years of experience in leading, managing or coordinating policy measures or projects;
three years of cumulative experience in one of the following areas: public policies for business innovation, export promotion, investment promotion, support to small and medium sized enterprises; • At least one expert has to demonstrate at least three years of cumulative experience in at least one of the following areas: public policies for financial market development, banking, insurance, micro-finance and other non-banking services, deposit and pension funds, financial reporting, accounting and auditing; • At least one expert has to demonstrate at least three years of cumulative experience in at least one of the following areas: public policies for commercial justice, private law, company law, in-court mediation, arbitration, insolvency procedures;
one year of professional experience related to interpreting and assessing the quality of enterprise statistics;
excellent drafting and reporting skills in English language (at least B2 level)
fluent in Georgian (at least B2 level);
At least twelve (12) years of experience in public policies to support economic development;
At least one professional experience with an EU budget support review in the field since 2015.
fully fluent in English and demonstrate both verbal and written skills in the language (C2 level);
""".replace(
    "• ", ""
).split(
    ";"
)

corpus = """
    8. Other Skills: Project Framework & Analysis (LFA); Research methodology; Academic Management; Word; Excel; Project, Power point
    9. In-country work experience: Bahrain, Bangladesh, Botswana, Benin, Burkina Faso, Burundi, Cambodia, Caribbean (Antigua/Barbados), China, Congo RDC, Egypt, India, Indonesia, Iran, Jordan, Malawi, Mauritius, Mongolia, Morocco, Mozambique, Namibia, Nigeria, Pacific (Fiji, Vanuatu, Solomon Island, Cook Island, Papua New Guinea), Pakistan, Romania, Rwanda, Senegal, Serbia, Seychelles, South Africa, Swaziland, Tanzania, Turkey, Uganda, UK, Vietnam, Zaire, Zambia, Zimbabwe.
    10. Present position:	Senior Consultant (Education and HRD)
    11. Client organizations: European Commission (EC); UNESCO, UNICEF, UNZA, World Bank. British Government - Dept for International Development (DFID), ENABEL; Government of Botswana; Government of Finland - Finnish International Development Agency (FINNIDA); Government of Japan (JICA); Government of Norway - Norwegian Aid Development (NORAD); Government of the USA – USAID; Bahrain Economic Development Board; British Council, Scottish Qualification Authority (SQA), RTI, Agence Belge de Développement (CTB/BTC).

11. Key areas of Education Support, Development & Training//Deployment:

Technical Advisor: Identification, Monitoring & Evaluation:
    • Country strategy identification/ formulation missions; Mid Term Reviews; Joint Annual Assessment reviews; Completion/ex-post evaluations to determine relevance, development efficiency, effectiveness, impact and sustainability. Familiarity with key quality criteria, assessment grid and standards framework.
    • Use of EC Evaluation and DAC models
    • Knowledge of results-oriented monitoring (ROM) system to assess programme performance – QA systems; monitoring process; eligibility criteria for project and regional programmes.
    • Familiar with EC, DFID, UNICEF and World Bank evaluation procedures (global thematic, MTR, ESSP, balance score card to manage performance, gender audits, PRSP) & indicator assessments (Evaluation Questions/Judgement Criteria (Global Thematic evaluation) and Value for Money/Value chains in different contexts.
    • Labour market surveys and signalling, and tracer studies
    • HIV/Information, Education & Counselling programmes - programme reviews, qualitative based ethnographic studies
    • Programme participatory workshop facilitation for needs identification (cause-effect) and strategy development
    • International tender dossier preparation & funding proposals, pre-qualifications and evaluations
    • Broad-based negotiation and professional skills to develop government ability to manage/monitor technical assistance support through capacity building strategies
    • Institutional business plans, programme frameworks, and financial/MTEF costing & analysis for CSOs/NGOs/projects

Technical Advisor: Budget Support and Financing Programmes for Education/Project Identification and Management:
    • Governance and policy development and strategic planning linked to programmatic implementation, resource and information management systems (Allocative efficiency in terms of defined national education objectives and priorities (PFM)
    • Identifying key management activities, drivers of change and operational functions to drive operational modernisation
    • International tender dossier preparation & funding proposals, pre-qualifications and evaluations
    • Develop government ability to manage/monitor technical assistance support through capacity building strategies

Technical Advisor: Technical and Vocational Education and Training and Labour Market:
    • Curricular renewal/assessment (Technical Vocational Education/Training)
    • Design of pilot literacy & numeracy skills programme & training support components. Initial literacy and numeracy and for occupational purposes (TVET/Entrepreneurship) with English as a Second Language (ESL)
    • Familiarity with technical modalities and levels of co-operation in Europe to promote quality assurance for Technical Education (Common QA Framework (CQAF), European Quality Assurance in Voc.Ed & Training (ENQA-VET), European Quality Assurance Reference Framework (EQARF), European Qualifications Framework, and CEDEFOP materials as well as with Develop a Curriculum Model (DACUM) and Systematic Curriculum & Instructional Development (SCID) programmes.
    • Environmental sustainability for TVET courses: international legislation, greening applications, biodiversity, compliance

Technical Advisor: Human Resource Development & Management:
    • National Human Resource Development Strategy (NHRDS) planning (deployment and redeployment) and skills diversification and restructuring. Organizational /human resources and management audits
    • Management competence audit & labour marketing/scoping future roles/services of providers. Linking VET and Training Standards to Employment and Macro-Economic Needs.
    • National Qualifications Frameworks (NQF + RPL), accreditation/certification & credit Quality Assurance (QA) systems for General Education (GE), TVET & professional training. Development of skills frameworks and occupational standards
    • Education management training & lifelong learning. Performance management audit & organisation and management systems development; school/community governance and accountability systems
    • Implementation (legal mandate, training authorities, university) of NQF strategies + wrap-around credit system for GE & TVT +NQF advocacy programmes
    • Information & Communication Technologies & blended/e-Learning in education development
    • Enhancing access and equity to professional development/deployment training programs

Technical Advisor: Policy, Strategy & Planning:
    • Sector Strategic Plan & Public Education & Management Indicators linked to MTEF/ PAF & Poverty Reduction Strategy
    • Sector wide policy formulation & approaches (SWAps) supporting Government policy/strategy analysis.
    • Sector reviews to promote planning & institutional reform leading to improved efficiency/effectiveness of resource allocation and education delivery systems. Sector reform process & strategy adjustments with focus on institutional/governance issues.
    • Programming/management of 7/8/9/10/11 European Development Fund (EDF) & ALA projects, Grants and NSA.
    • Support to strengthen sector coordination between government, development partners and civil society.
    • Value-for Money audit – efficiency, effectiveness, sustainability and economy of TVET institutions (commercial/mechanical/construction/ agricultural) in Upper Katanga/Lualabe. Assess ministry institutional capacity and follow-up labour market employment requirements to meet local labour needs of public-private partnerships and disadvantaged/gender groups.  
    • IEMA assessment of training course - ‘Sustainability Skills for Managers’
    • Phase 2: Assessment of selected full proposals (Europe, Africa, Asia, Pacific) to ENABEL – Belgian Development Agency for support to the VET Toolbox - ‘Innovative Strategies and Approaches to Improve Employment Opportunities for Disadvantaged and Vulnerable Groups through Vocational Education and Training (VET)
    • Technical advisor - Develop Due Diligence Questionnaire (DDQ) and Intellectual Property Rights contracts covering environmental consultancy issues.
    • Phase 1: Assessment of 73 funding requests (Europe, Africa, Asia, Pacific) to ENABEL – Belgian Development Agency for support to the VET
    • Identification and Formulation of EU Actions in Support of Education Sector Reforms In Egypt under The Annual Action Programme 2019. Expanding Access to Education and Protection for at Risk Children in Egypt".
    • Training quality evaluation. External assessment of environmental skills for sustainability training programme and tutorial quality of presenters. IEMA Institute of environmental management and quality control assessment certification.
    • Back-up management on flexible benefits programme and associated provider relationships related to interface with providers/HR team (London councils).
Final Evaluation of Education Sector Support Programme (ESSP), Analytical Capacity and Development Partnerships (ACDP) Programme and Minimum Service Standards Capacity Development Programme (MSS CDP) through a national theory of change/ assumptions.
    • Technical advisor - Formative Evaluation of the Out-of-School-Children Initiative (OOSCI) to determine progress made towards realizing OOSCI objectives, its relevance, and effectiveness, and to test the validity of the OOSCI theory of change and its assumptions, and strengthen the programme logic.
    • Assessment of the eligibility/relevance of Cambodia’s Education Strategic Plan (ESP) 2017-8 to gauge the continued complementarity of European Union budget support to MoEYS as per the Technical and Administrative Provisions Education Sector Reform Partnership 2014-18.  Assessment of variable tranche target indicators for funding/PFM
    • Rapport de la revue a Mi-Parcours: Projet D’appui aux Organisations Béninoises par le Renforcement des Compétences des Ressources Humaines (PAORC) utilisant les 5 critères d'évaluation du CAD  de l’OCDE pour analyse
Technical advisor - Identification with a focus on ECD and Basic education to facilitate strategic interventions to action data from tracking and tracing of learners throughout the sectors; and to support the diversification in learning pathways that respond to different learning styles to enhance career opportunities and continuous professional development,
    • End-term Review of the Improving the Training of BTVET Technical Teachers/Instructors, Health Tutors and Secondary Teachers in Uganda (TTE) programme in terms of Relevance and sustainability of the teachers’ professional development system (ATL and mentorship trainings, pilot support supervision system) linked to professional classroom incentives ; strategies to strengthen management capacities of TIET and colleges’ staff;
strategies implemented to design colleges’ new infrastructure
    • Technical advisor -Review of the Institutional professional capacity building process and political economy for local government administration, natural resource management and education. Assessment of institutional/ organizational benefits – Local Government Administration & Natural Resource Management.
    • Technical advisor -Development of web-based Blended Learning content/approaches for organizational capacity and skills training support system programmes with linkages to professional classroom incentives/school support mechanisms and inspections/teacher induction
    • Review of MoE structural re-organization at central and field directorate levels and readiness for change through working groups
    • Tender methodology proposals (EU) to support the provision of Technical Assistance to Improving Secondary Education (ISEM) – teacher needs analysis, school/teacher support frameworks, and inspectorate support
    • Technical advisor -Education planning and reform in developing countries focusing on decentralization and public sector reforms; Teacher Training and Development in Africa and Asia.
    • Revue a Mi Parcours de L’intervention ‘Renforcement Des Capacités Organisationnelles Par L'Octroi De Bourses’ (PRECOB) utilisant les 5 critères d'évaluation du CAD ET MTEF: dispositif organisationnel de l’intervention ; synergies avec les autres interventions mises en œuvre par la CTB et les partenaires internationaux; contribution des programmes dans la prise en compte des thèmes transversaux (genre et environnement) ; Considération des initiatives de développement de séquence de valeurs et des options d’évolution de marché.





    • SME development & Business Leads – eligibility for EU/Govt support; Skills Development in SMEs + training & mentoring networks (Business Planning; Promotion Research;/Finance Information Human Resources/Entrepreneurship).

    • Technical advisor - 2nd Phase NQF – Framework development (Levels/Descriptors/QA/Credits/Audits/RPL) for general. TVET and Higher Education: Governance & Management – Operational Plan & deliverables; Pilot phase & establishing a Qualifications Authority + legal mandate; Change Management Plan + Communication & Promotion Plan; Impact Assessment + Monitoring & Evaluation Plan.
    • Annual Assessment/analysis of the first tranche of the EU-Cambodia Education Sector Reform Partnership (ESRP) 2014-16 and eligibility assessment component for the Cambodia Education Sector Plan 2014-2018. Re-assessment of 2013 ‘un-met targets’.
    • Institutional assessment (gap & performance analysis) of the Barbados Accreditation
 Council (BAC) to assume role of qualifications authority and legislation to determine its
 effectiveness for implementation of the NQF. Inception design of national qualifications framework (NQF) aligned to CARICOM framework and compatibility to EQF.
    • Annual Assessment of the 2013 SPSP EU-Cambodia Education Sector Policy Support Programme (2011-13) and eligibility annexe. Eligibility Assessment for Cambodia Education Sector Plan 2009-13
    • Support and quality assurance to on-going contract for standardization of pay and contracts of VT tutors (University of London).
    • Mid-Term Review of the EU-Cambodia Education Sector Policy Support Programme 2011-13 and Support to the formulation of the new Education Programme (indicators) for Budget Support/Sector Reform Contract and issues of complementarity (UNICEF, UNESCO, VVOB, JICA)
    • Technical advisor - School Grants programme design. Situational analysis of fees and levies: school level context & school minimum standards (access, quality, infrastructure, continuous professional development, hard-to-reach communities, teacher remuneration), existing legislation & statutory provisions, complementarity with other donor programmes.
    • Concept design of school grants programme. Type of school grants, objectives, criteria for approval of the schools’ grants, management and policy (school level management and governance + ministry and district level capacity support), monitoring and evaluation (data management and collection).
    • Design of pilot phase and roll-out within a monitoring and risk analysis framework
    • Support mission to Namibia for the mid-term ETSIP Annual General meeting leading to sector budget support (Sector Reform Contract) disbursements. Review of Aide Memoire and the Education Sector Strategic Plan – PFM; HIV/AIDS; VET; ICT; Life-Long Learning; Basic and Higher Education. Review of MoE Strategic Plan
    • Support mission to Papua New Guinea (PNG) for the preparation of the Phase2 HRDP education sector programme (Action Fiche/TAPS/LFA) and to support the process of quality assessment by the Quality Steering Group (QSG) in Brussels
    • Final Evaluation of the PRIDE (Pacific Regional Initiatives for the Delivery of Basic Education (efficiency, effectiveness and the impact of implementation modalities)
    • Technical advisor -Coordination, HR and financial/MTEF management of the regional programme. Institutional arrangements within USP and stakeholders involvement. Development partner complementarities (EC, NZAID, AusAID, UNDP). Sustainability of outputs at regional level
    • Report commissioning the work on developing & implementing occupational standards for Bahrain to enable it to match best practice regulatory/development arrangements.
    • To assess strategic objectives for the project and development of governance/legislation arrangements to promote employment in response to labour market needs/management
Assessment Report on the Implementation of Education Reform Action (ERA) Plan 2009-2010, in preparation for the development of a Medium Term Education Sector Strategy.
    • Technical advisor - Policy/strategy implementation within Ministry of Education, Employment and Human Resources (MEEHR) planning linked to programmatic implementation, information management systems & National Human Resource Development Strategy including teacher remuneration, career outlook, gender mainstreaming, new teacher induction, inspectorate support. Assessment in terms of achievements under the ERA Plan.
    • Technical advisor - Analysis of constraints and implementation needs for Medium Term Education Strategy 2011-2015 - engagement/ownership; resourcing & financing; reform environment; human resources development; legal framework development; monitoring/ evaluation
    • Review of Technical & Vocational Education & Training provision (legal/institutional human & financial resourcing/public-private partnerships/labour-market/competency based training/quality assurance & qualifications framework/ development partner support & harmonization) with reference to disadvantaged groups.
    • Capacity development within framework of development partner/GPE/civil society mutual programmes
    • Formulation/drafting of Action Fiche/TAPS etc with regard to TVET and grants to support sustainable livelihoods & protection of environment.
    • Technical advisor - To assist the BAMC with the development of an HR re-organization plan and staff training needs aligned to the Barbados National Report on Technical and Vocational Education and Training (TVET) and National Policy Framework for TVET in Barbados (Investing in our Future) (June 2003), and complementing the NVQB User Guide.
    • Write tender methodology proposal to re-establish and strengthen institutional and professional capacity in TVET to meet labour market, macro-economic and social needs with focus on Construction & Tourism.
Technical advisor - Thematic global evaluation of European Commission support (global and sector budgets) to BASIC EDUCATION in the education sector in partner countries 2000-7 in terms of logic, coherence & relevance of EU objectives and to the needs of recipient countries taking account the institutional capacity required to maintain consistent levels of access, service delivery & EC value-addedness.
    • Review of draft inventory of EC Basic Education (Primary & Junior Secondary) global (ACP, ALA etc) contracts & of impact diagrams consonant with policy priorities
    • Attainment of MDGoals and EFA targets & inclusive education & review of JAA country assessments
    • EC-based evaluation interviews with DG-Relex, DG-AIDCO, ALA, & desk officers
    • Country strategy/Action Plans evaluations – Vietnam, Bangladesh
    • Analysis of findings (on basis of JCs & EQs) & presentation to EC Reference Group
Ref: http://ec.europa.eu/europeaid/how/evaluation/evaluation_reports/2010/1282_docs_en.htm
    • Institutional Twinning for the National Authority for Quality Assurance and Accreditation of Education in Egypt.
    • Assessment of needs and review of ongoing Quality Assurance standards and platforms, and quality assuring professional capacity in General Education, TVET and Higher Education including e-Learning.
    • Consultation with ETF, SQA and other agencies in the field.
    • Technical advisor - Handover of technical assistance to assist to establish the Botswana National Credit & Qualifications Framework to strengthen the National Human Resource Development and Economy
    • Assessment of EC Basic Education support 2000-2007 in relation to MDGoals & EFA targets, government PRSP (PEDP, NFPE, BRAC and NGOs) and Continuous Professional Development/Incentivization of teachers – field phase
    • Write tender methodology proposal (World Bank) to support VET Quality Assurance, Accreditation & Development of NQA/NQF under IPA 2000
    • SADC regional workshop on Accreditation and Certification to harmonize qualifications in the region as part of NCQF.
    • Lead NQF benchmarking tour to Namibia/Mauritius Qualifications Authority & Mauritius HRDC as examples of middle income country developments and small island development.
    • Attend Mauritius National Human Resource Development Strategy (NHRDS) workshop
    • Benchmark report
    • Technical advisor - Technical assistance to assist to establish the Botswana National Credit & Qualifications Framework. Work plan preparation, HR planning & staffing.
    • Review of Quality Assurance procedures for Higher Education & TVET sectors to ensure build up of local capacity and global/regional market recognition
    • Compatibility & alignment between separate quality assurance processes to ensure coherence/ comprehensiveness similar to EQARF for VET.
    • Staff mentoring/capacity-building of NQF project unit
    • Lead stakeholder technical revisions of NQF & credit matrix (TVET and Higher Education)
    • SADC regional workshop on Accreditation and Certification to harmonize qualifications in the region.
    • Lead NQF benchmarking tour to Namibia/Mauritius Qualifications Authority & Mauritius HRDC as examples of middle income country developments.
    • Governance/management structure & mandate for legislation of a Botswana National Qualifications Authority
    • Write tender methodology proposals (EU) to support the Improving Quality, Access and Governance programme
    • Write tender methodology proposal (EU) to strengthen the Vocational Qualifications Authority & NQF system
    • Review GoB National Human Resource Development Strategy programme to assess appropriate areas for EU support linked to internal stakeholder institutional & World Bank support
    • Assist to establish indicators with EC Delegation and GoB (various ministries) for EDF 10 based on Vision 2016, NDP10, National Human Resource Development Strategy/ Country Strategy Education Policy Notes, Education Performance Expenditure Review, PEFA targets. Attention given to rural out-of-school/disenfranchised youths from minority ethnic groups and gender issues
    • Assist to develop policy dialogue issues between EC Delegation and GoB to enhance GoB accountability and for Sector Budget Support/Sector Reform Contract
    • Assist with identification/formulation/drafting of 10th EDF €62M HRD SPSP (TAPS/ Action Fiche etc) with regard to Primary school teacher development, TVET, Labour Market, the National Human Resource Development Strategy and Special Education Needs.
    • Final Joint Annual Appraisal ‘Catch-up tranches’ (JAA) of the 9th EDF Sector Policy Support Programme (E&T) with GoB & EC to assess relevant policy issues against agreed targets for key indicators & determine EC financial support
    • 2008&09 Joint Annual Appraisal (JAA) (monitoring) of the EDF9 Sector Policy Support Programme (Education & Training) with GoB & EC to assess relevant social/ education policy issues (Basic Education & inclusiveness, TVET, NQF, Labour Market.)
    • Assessment of AID India (Tamil Nadu) program for replication.
    • Develop guideline criteria of the AID India literacy/numeracy program for replication.
    • Write tender methodology proposals to support the provision of Technical Assistance for support to the Development of an Education Management Information System (EMIS) for the Federal ministry of General Education(FMOGE)
    • Technical advisor - Capacity-building programme for Madirelo Training & Testing VET Centre to develop national occupational standards and unit standards for Electrical Engineering; Mechanical Engineering; Hotel & Catering; and Entrepreneurship for the BNVQ Framework.  Develop mechanisms to support staff, students & industry
    • Assist the Botswana Training Authority (BOTA) to re-structure the system for the development of occupational standards and standards setting task forces (SSTFs) for TVET on a regional basis
    • Technical advisor - Promote course programs alignment to competence-based modularized training (CBMT) to promote market recognition and to attract global investment.
    • Review DACUM process and assessment of National Craft Certificate (NCC) qualifications
    • Liaison with Ministry of Labour/ Ministry of Finance, Development & Planning.
    • Mid-Term Review of the 8th. EDF Support to Technical and Vocational Education and Training in Botswana (8 ACP BT)
    • Assessment of EU support to Technical Training Colleges – buildings, equipment and training programmes.
    • Assessment of EU support to Special Education Needs groups in Technical Training Colleges
    • Technical advisor - Diagnostic Assessment for a review of the national apprenticeship and trade testing schemes (unit standards).
    • Analysis of staff technical expertise and formulation for capacity building project for Madirelo Training & Testing VET Centre and Botswana Training Authority aligned to MTT strategic direction and Botswana’ national HR strategy.
    • Preparation of methodology proposals to support the on-going reform of the education sector – inspectorate/primary & secondary/EMIS/teacher motivation.
    • Write tender methodology proposals to support Vocational Education and Training, labour market, career & guidance and Life Long Learning systems
Preparation and facilitation of ACP Regional Education and Health Seminar 2007 for the European Commission (AIDCO) re:
    • International policy context. (Paris Agenda, Brussels Framework for Action on Education, FTI, Global Fund, SWAps, governance) & drivers of change.
    • Evidence-based policy formulation for development partner dialogue
    • Financing modalities (GBS, SBS etc) & appraisal of national strategic plans & JAA linking  with governance, poverty reduction (PRSPs) & MDGs/EFA targets.
    • Monitoring: Role of/best practice in joint sector reviews and PRS reviews; linking policy dialogue with implementation; setting indicators for effective dialogue & results-oriented management (education).
    • Preparation of methodology proposals for WB and EC funding for sustaining & expansion of the Accelerated Education Systems (AES) in southern Sudan within a multi-donor funding context.
    • Technical advisor -  ‘Aligning an NQF with the European Qualifications Framework’. Seminar to promote the establishment of a National Authority for Qualifications’ to key national/international stakeholders.
Ref: http://www.cnfpa.ro/Files/phare/Presentation%203-%20Armand%20Hughes.ppt#261,1,
Alinierea cadrului naţional al calificărilor la EQF
    • Graduate Tracer Study/assessment of the Botswana Technical Education Program (BTEP) to assess the: employability of graduates, destination & employment rates of graduates; employer satisfaction with BTEP
    • Assess degree of consonance between labour market needs and demand & programme design.
    • Assess performance of BTEP implementation in Technical Training Colleges
State Education Sector Project (SESP)
    • Preparing technical papers, work plans and cost tables for Capacity Development for Management & Planning sub-component as part of the Institutional Development program for State Ministries of Education for Kano, Kaduna & Kwara.
    • Assist with preparations for World Bank appraisal mission.
    • Systems evaluation of teacher training for Cambridge TKT certification & on-line blended education ESP business program. Proposal for training of trainers/teachers
Feasibility study & analysis for a National Credit & Qualifications Framework (NCQF).
    • Design & conceptual base for NCQF with linkages to SADC protocol, ISCED & European Qualifications Framework
    • Institutional infrastructure & technical approaches for implementation & Quality Assurance structures
    • Compatibility with regional practice/industry needs
    • Team support to regulatory/legislative arrangements & economic/financial (MTEF) viability.
    • Project memorandum preparation
Ref: botswananqa.com/documents/2006%20Cardno%20report.pdf
Preparatory activities for 9th EDF Education Training Programme (€20M). Start-up (10 months phase)
    • Assistance to the Ministry of Education with pre-implementation programme assessments & planning (Programme Estimates/Global Operational Plan; Drafting tender dossiers) & tender preparation
    • Develop TAPS for ongoing phase
    • Design of pilot capitation grant/formula funding with emphasis on Orphans/Vulnerable Children & ‘whole school’ trainer & governance programme
    • Design of pilot literacy & numeracy skills programme & training support components. Assessment of the HR/EMIS/TSC needs; Staff Performance management & Quality Assurance; Performance Management System (PMS) impact
    • Technical assistance to the Rwanda Sector Support Programme 2005-2010
    • Assistance to MINEDUC to develop Education Sector Strategic Plan (ESSP) 2005-2010 & 5 year financing plan/MTEF & SWAp linked to PRSP & World Bank HIPC initiative
    • Follow-up on key issues wrt Science & Technology policy & National VET Strategy
    • Strengthening capacity within the Ministry of Education (MINEDUC) to manage the planning, coordination, monitoring & JRES review process (Joint Review of the Education Sector).
    • Following up key policy development issues – Nine Year Basic, Post Basic Education & Training, EFA targets & MDGoals, SEN, Adult Literacy, and Technology
Education/HRD sector Identification Study (EDF9 €16M) within a budget support framework & evaluation of TVET strategy provision. Botswana National Skills Development Strategy (expansion/improved access).
    • Pre-Feasibility study & participatory workshop
Tender preparation for EDF9 (EDUTRAIN) project with emphasis on Grades 7&8 curriculum development & teacher in-service
    • Development of provincial web-based monitoring & performance reporting system linked to EMIS.  Review of ICT programme linked to EMIS
    • Formulation Mission for EC Support to Education Sector (€12M)
    • Institution building at macro-management level (Ministries of Education, Finance, Planning & Investment) leading to targeted budget support & mechanisms of accountability for MTEF/PFM.
    • HR/Financial management – Personnel (PMIS) & Financial Management Information System (FMIS) (national & decentralised)
    • Whole-school development & women managers incentivization
    • Develop ALA Financing Proposal, TAPs, PCM, log-frames, EcoFin analysis & tender dossier
    • Education/HRD sector Feasibility Study/evaluation (EDF9) to assess the upgrading and in-service needs of Education Centres.
    • Education/HRD sector Feasibility Study (EDF9), & Financing Proposal (€24M) Primary/EFA Financing Proposal, TAPs, PCM, log-frames (LFA) & full tender dossier moving towards budget support (Sector Reform Contract) / programmatic aid.
    • Primary sector financing reallocation & cost saving/shifting reforms. Capitation grants linked to Quality Assurance, and reform of early primary program (school-base INSET, teacher training & curricula reform). Teacher Resource Centres & INSET programs.
    • Participatory workshop - education development strategy identification & stakeholder analysis.
    • Design of QA & Accreditation benchmarking system & framework with implications for profiling for Core Service Suppliers (INSET, Curriculum Design Centre, Teacher Training Colleges & Core Implementers)
    • Capacity evaluation/indicators of MOET units.
    • Education sector program (primary/EFA) – teacher training recruitment programs & curriculum renewal
    • Capacity-building with Ministry of Education (MOET) Project Management Unit (PMU)
    • Project Teacher education program preparation for university/MoE teacher education faculties. Project assessment and global planning.
    • Stakeholder (MoE, Universities Belgrade & Sombor) participatory workshops to assess work skills to match Teacher Accreditation Audit (Subject matter & Pedagogical knowledge; Technology) and Institutional INSET Accreditation; Capacity building; Curriculum; Facilities & equipment; Administration; Recruitment & admissions)
    • Development of guidelines on the formulation of national Primary Education Development Programs (PEDP) & scoping of intervention areas for development partners
    • Development/cost analysis - country program
    • Programming & cost analysis: Bac Giang province pilot project formulation
Identification/Appraisal to formulate HRD
    • Education sector program (EDF9)+tender dossiers
    • Quality provision of primary education;  teacher training; HIV/AIDS; TVET
    • Participatory workshop to identify Broad Areas of Possible Intervention (BAPIs).
    • Development of SADCC TVET identification proposals for training/entrepreneurial programs for multi-donor funding.
    • NQF, teacher accreditation & profiling, QA
    • Key MoE member workshops to assess logframe proposals (QA, HRD, Skills development, NQF, Access)
    • Labour market needs assessment
Proposals & log-frames for EU Revenue Services funding
    • Sector analysis & Ministry audit. Key areas of intervention plans - planning/ decentralization; teacher development curriculum renewal/ Quality Assurance
    • Macro-planning for ‘Education Development Strategy   2001-2010’ policy & implementation
‘European Union – Vanuatu Education Development’ Program (EUVED)/Junior Secondary Schools' Expansion (EDF8). A €8.3M project to rehabilitate 18 new schools on 12 islands; to expand the Vanuatu Teachers’ College, new library complex, & Examination Centre; and to ensure effective utilisation of educational buildings through EUVED education.
    • Decentralised project management (project definition/supervision; financial control; annual/global work plans & budgeting; resource allocation; tender preparation/pre-qualifications/assessments; contract preparation; team supervision; planning for post-project operations & commissioning)
    • Development of school-based management programmes and assistance to the pre-service primary training college (literacy and First language learning materials)
    • Policy assistance to the MoE to revise teacher grading/promotion structure & training. (Teacher career patterns - Profiling teacher profession; Career development patterns; Organisational constraints to teacher development). Professional Development & Accreditation design. Teacher career recognition/promotion
    • Institutional support (EMIS/Project/Evaluation) to Planning & Policy Unit (MoE)
    • Economic & social development planning: EDF 9 & Structural Adjustment Program Vanuatu
Ref http://ec.europa.eu/development/icenter/repository/179_ACP_EU_en.pdf page 55
In-country assessment for consulting services /implementation of World Bank IDA credit:
    • 1. Basic (Fourth) Education program, with focus on Community School improvement.
    2. Population & Health Promotion program
In-country tender preparation for EUVED Education Development Program (EDF8)
Identification of sector-wide needs (Health, Social Welfare, Public Administration, Development Management) and criteria for Technical Co-operation & Training awards
    • Skills assessment and development of benchmarks compliant with the National Qualifications Framework (NQF) for financial institutions.
    • HRD training project for NQG and Skills Development Bill compliance
    • Identification of training programs for social welfare sector.
    • Student outcome evaluation of DFID Technical Co-operation Training, & review of management efficiency of award program.
    • Review of modalities of information & development co-ordination between EC Delegation, EU Member States, & S.A Govt.
    • Management assessment audit of the Education Foundation to scope (EMIS/GIS) future role within the Dept of Education in relation to labour market needs.
    • TVET skills development audit and review of GoA labour market survey. Education sector analysis and project identification/design for Technical & Financing (€4.5M) proposal (EDF8) with a focus on technical/vocational training (TVET) with regard to:
    • Youth Skills Training Programme (YSTP) - testing, linkages to employers; curriculum development; trainer training, staff retention incentives, counselling/life skills, & rehabilitation of the National Technical and Vocational Centre;
    • Appraisal mission (Technical & Financing) to develop pre-service trainer training program & school-based in-service cascade pilot program for primary education (E7M)
    • Teacher education sector analysis for NWFP. Teacher education strategy/policy formulation for pre-service/in-service teacher education, teacher supply-demand, hard-to reach communities, gender mainstreaming of teacher supply
    • Issues of female recruitment & in-post barriers. (World Bank; SAPP IDA credit)
    • Strategies to promote girl school enrolment
    • Outcome & Impact evaluation of NGO HIV/AIDS peer education program. UNICEF support policy & activities assessment workshop
Ref:  http://ideas.repec.org/a/eee/epplan/v25y2002i4p397-407.html
    • Skills assessment and development of benchmarks in the banking sector compliant with the National Qualifications Framework (NQF) for financial institutions.
    • HRD training project for NQF/Skills Development Bill compliance for the banking sector
    • Management needs assessment & management workshop programme for senior managers/trainers in agricultural colleges to improve vocational education performance
    • Development of training modules in Planning & Management for senior MoE officials to facilitate decentralisation in government institutions (Public Sector/ Budget Reform Prog)
    • AIEMS Project activity-to-output review. A £12.7M project managed by the British Council to improve schools & establish a network of resource centres.
    • NGO operations and management review, and role assessment within national Language in Education policy
    • Tender preparation for EU-funded provision of technical assistance Services for University of North Science Foundation Year (UNIFY)
    • Summative report. Teacher-pupil outcome evaluation of Molteno (literacy) materials for primary schools
    • Needs assessment of in-service management and supervision at school and zonal levels for Malawi School Support Systems Project.
    • Implementation & monitoring of library learning materials & technology support in Technical Training Institutes. Development of library management program
    • Outcome evaluation report on effectiveness of AIDS education project activities by NP Health Education Project.Field-based training of Health Education field workers in impact/outcome evaluation and monitoring techniques
    • Zambian Education Research & Networking Project. Task-based training workshop on supervision techniques and qualitative research methodologies – Faculty of Education.
    • Formative evaluation of Molteno program. HRD diversity action evaluation of the Project’s R& D Unit.
http://www.molteno.co.za/index.php?option=com_content&view=article&id=51&Itemid=60
    • Rehabilitation of Primary/ In-service Teacher Training colleges and libraries (physical structures and classroom/ science/learning tech equipment). Inception report. EDF7
    • Social Sector Appraisal Report. Review of Phase 2
    • Implementation & monitoring of the Library Support Program for Primary & Secondary Teacher Training Colleges. Methodology-across-curriculum development.
    • Formulation of a national professional development strategy for training
    • Supportive infra-structure for innovation and to assist with the implementation of new course structures, syllabi and examinations for colleges, and teacher profiles for accreditation
    • Teacher assessment at school/college level. School Quality Performance Indicators.
    • Management of training & trainer training programs
    • Teacher motivation and career support
    • Sustainable development framework for the project and training for counterparts
    • Base-line study of trainee teachers’ cognitive/linguistic entry level competence
    • INSET orientation on management of change for Provincial/District Education Officers
    • ELT curriculum renewal project on INSET courses for rural teachers (RCDM, Uganda)
    • Development of post-graduate course module -`Paradigms of Research and Research Skills' (University of Sheffield - outsourced)
    • Course Director for English for Academic Purposes (EAP) & Post-graduate MBA academic skills induction programs (University of Sheffield - outsourced)
    • English for Special Purposes (ESP) - Management, Banking, Computer Engineering etc.
NGO to support mainly black primary school teachers
    • Policy, finance, staff management and institutional administration
    • Inception planning and development of the Farm School Project
    • Project coordinator of INSET programs for teachers in black primary education: East Rand Teacher Training Project; Mamelodi Teacher Training Project; Gazankulu training programs
    • Administration & management of EFL schools
    • Academic program director
    • Staff management (42 lecturers) & academic program director
    • Pre-sessional EAP course director & Dip.Ed TEFL teacher trainer
    • ESP materials development coordinator.
    • English as a Foreign (EFL)/Second Language (ESL) – Proficiency and First Certificate level

""".replace(
    "    • ", ""
).split(
    "\n"
)
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

top_k = min(2, len(corpus))

for query in queries:
    query_embedding = model.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    for score, idx in zip(top_results[0], top_results[1]):
        print(corpus[idx], "(Score: {:.4f})".format(score))
