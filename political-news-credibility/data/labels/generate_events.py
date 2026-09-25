# This file contains only events with IMMEDIATE (0 days) or CLEAN (1-7 days) outcomes
# for high causal clarity and reliable source_correct labels.

# - Single clear incident triggers event  
# - Outcome within 0-7 days
#
import csv
from pathlib import Path


HISTORICAL_EVENTS = [
    # ── 1. Boris Johnson faces Conservative Party no-confidence vote af... ──
    {
        "description": 'Boris Johnson faces Conservative Party no-confidence vote after 54 MPs submit letters to 1922 Committee',
        "event_date": "2022-06-06",
        "outcome": 'Johnson won the confidence vote 211 to 148; he resigned six weeks later on 7 July 2022 following the Pincher scandal',
        "outcome_date": "2022-06-06",
        "topic_category": "leadership",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Johnson faces existential threat to his premiership as confidence vote triggered by rebel MPs',
                "framing_label": "crisis",
                "correct": False,
            },
            {
                "source_name": "bbc",
                "headline": 'PM expected to survive confidence vote but authority will be severely damaged',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Boris Johnson will comfortably defeat backbench rebels in confidence ballot tonight',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": 'Johnson to survive no-confidence vote but MPs signal growing unease with his leadership',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Result on knife-edge as PM fights for political survival in confidence ballot',
                "framing_label": "crisis",
                "correct": False,
            },
            {
                "source_name": "reuters",
                "headline": 'UK PM Johnson faces confidence vote as Conservative MPs lose faith in leadership',
                "framing_label": "crisis",
                "correct": False,
            }
        ],
    },
    # ── 2. CCTV footage published showing Health Secretary Matt Hancock... ──
    {
        "description": 'CCTV footage published showing Health Secretary Matt Hancock kissing aide Gina Coladangelo in breach of Covid social distancing rules',
        "event_date": "2021-06-25",
        "outcome": 'Matt Hancock resigned as Health Secretary on 26 June 2021, the day after the CCTV images were published by The Sun',
        "outcome_date": "2021-06-26",
        "topic_category": "scandal",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Hancock must resign immediately after CCTV footage shows blatant breach of the Covid rules he imposed',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'PM backs Hancock despite affair revelations but political pressure intensifies',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "telegraph",
                "headline": 'Hancock apologises for affair and social distancing breach as PM retains confidence in minister',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": "Hancock's position increasingly untenable as colleagues publicly demand he resign",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Mounting calls for Hancock resignation after lockdown rule breach exposed',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK health minister faces resignation calls after Covid rule breach revealed',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 3. Dominic Cummings travels from London to Durham and Barnard C... ──
    {
        "description": 'Dominic Cummings travels from London to Durham and Barnard Castle during strict national lockdown restrictions',
        "event_date": "2020-05-22",
        "outcome": 'Cummings did not resign following the Barnard Castle incident; he left Downing Street in November 2020 following an internal dispute',
        "outcome_date": "2020-05-25",
        "topic_category": "scandal",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Dominic Cummings must resign for damaging the lockdown rules that everyone else followed',
                "framing_label": "crisis",
                "correct": False,
            },
            {
                "source_name": "bbc",
                "headline": 'PM stands by Cummings despite 63 per cent of public saying adviser should resign',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Cummings acted reasonably in difficult circumstances and PM is right to stand by him',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": 'Johnson stands firm behind Cummings despite cross-party calls for resignation',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Cummings resignation demanded by MPs across parties as lockdown row deepens',
                "framing_label": "crisis",
                "correct": False,
            },
            {
                "source_name": "reuters",
                "headline": 'UK PM defends top adviser amid uproar over lockdown journey to Durham',
                "framing_label": "routine",
                "correct": True,
            }
        ],
    },
    # ── 4. Owen Paterson MP found to have breached lobbying rules; gove... ──
    {
        "description": 'Owen Paterson MP found to have breached lobbying rules; government attempts to rewrite standards process to protect him from suspension',
        "event_date": "2021-11-03",
        "outcome": 'Owen Paterson resigned as MP on 5 November 2021; the government U-turned on its attempt to rewrite the standards process within 24 hours under intense political pressure',
        "outcome_date": "2021-11-05",
        "topic_category": "scandal",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Government attempt to rescue Paterson triggers sleaze crisis engulfing the Conservative Party',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Paterson cleared by government vote but watchdog and opposition condemn standards overhaul',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Paterson case shows parliamentary standards system needs reform, government argues',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": 'Furious backlash expected to force government retreat on controversial standards vote',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Paterson resignation imminent as sleaze scandal overwhelms government handling',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK government faces political crisis over attempt to save MP from standards penalty',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 5. Deputy chief whip Chris Pincher resigns after allegations he... ──
    {
        "description": 'Deputy chief whip Chris Pincher resigns after allegations he drunkenly groped two men; Johnson knew of prior complaints before appointing him',
        "event_date": "2022-07-01",
        "outcome": 'The revelation that Johnson had been warned about Pincher triggered mass cabinet resignations; Johnson resigned as PM on 7 July 2022',
        "outcome_date": "2022-07-07",
        "topic_category": "scandal",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Pincher scandal threatens to bring down Johnson government as truth of prior warnings emerges',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'PM faces questions over appointment of Chris Pincher despite awareness of prior allegations',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Pincher resigns after groping allegations but government insists PM was not briefed',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": 'Government in deepening crisis as ministers demand PM explain his knowledge of Pincher complaints',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Mass resignations signal end of Johnson era as Pincher crisis rapidly escalates',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK government destabilised as cabinet ministers resign over handling of Pincher scandal',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 6. Brexit post-transition trade deal negotiations reach final
    {
        "description": 'Brexit post-transition trade deal negotiations reach final stage with fishing rights and level playing field as key sticking points',
        "event_date": "2020-12-20",
        "outcome": 'UK-EU Trade and Cooperation Agreement signed on 24 December 2020 before the transition period ended on 31 December 2020',
        "outcome_date": "2020-12-24",
        "topic_category": "policy",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Brexit deal breakthrough possible as both sides show willingness to compromise on fishing and competition rules',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'UK and EU in final talks as no-deal looms but last-minute agreement still possible',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Britain ready for no-deal as EU demands unacceptable concessions on fishing in final hours',
                "framing_label": "wont_happen",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": 'Last-minute deal possible if both sides compromise on level playing field dispute',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "financial_times",
                "headline": 'Brexit deal odds improve as fishing compromise emerges during overnight talks',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK and EU race to seal post-Brexit trade deal before Christmas deadline',
                "framing_label": "will_happen",
                "correct": True,
            }
        ],
    },
    # ── 7. Humza Yousaf terminates the SNP-Green Bute House Agreement, ... ──
    {
        "description": 'Humza Yousaf terminates the SNP-Green Bute House Agreement, triggering a confidence motion from opposition parties',
        "event_date": "2024-04-25",
        "outcome": 'Humza Yousaf resigned as First Minister of Scotland on 29 April 2024 before the confidence vote took place',
        "outcome_date": "2024-04-29",
        "topic_category": "leadership",
        "sources": [
            {
                "source_name": "guardian",
                "headline": "Yousaf's position untenable as Scottish Greens withdraw support and confidence vote looms",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Scottish FM faces no-confidence motion as Green coalition collapses and opposition unites against him',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Yousaf scrambles for votes as SNP faces leadership crisis after Green coalition split',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": 'SNP leader expected to lose confidence vote as parliamentary arithmetic turns decisively against him',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Yousaf remains defiant as confidence vote approaches but numbers look impossible to find',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "reuters",
                "headline": 'Scotland First Minister faces confidence vote after collapsing Green coalition deal',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 8. Suella Braverman publishes article in The Times claiming pol... ──
    {
        "description": 'Suella Braverman publishes article in The Times claiming police treat pro-Palestinian marches more favourably than other groups',
        "event_date": "2023-11-09",
        "outcome": 'Suella Braverman was sacked as Home Secretary on 13 November 2023 following the publication of the article without Prime Ministerial approval',
        "outcome_date": "2023-11-13",
        "topic_category": "cabinet",
        "sources": [
            {
                "source_name": "guardian",
                "headline": "Braverman must go after incendiary article on policing undermines PM's authority and party unity",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Home Secretary under serious pressure after Times article written without PM approval',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Braverman raises legitimate and long-overdue concerns about policing of protest that others fear to voice',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": "Braverman's cabinet position precarious after article published without Downing Street clearance",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Sunak faces mounting pressure to sack Home Secretary over unauthorised Times article',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK Home Secretary faces cabinet pressure after publishing article without Prime Minister approval',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 9. BBC reports that NatWest CEO Dame Alison Rose personally bri... ──
    {
        "description": "BBC reports that NatWest CEO Dame Alison Rose personally briefed a journalist about Nigel Farage's Coutts account closure",
        "event_date": "2023-07-25",
        "outcome": 'Dame Alison Rose resigned as NatWest CEO on 26 July 2023 after admitting she had personally briefed the BBC journalist',
        "outcome_date": "2023-07-26",
        "topic_category": "corporate",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'NatWest CEO personally briefed BBC on Farage account in serious breach of customer confidentiality',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Dame Alison Rose apologises for Farage briefing but hopes bank can move beyond the crisis',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "telegraph",
                "headline": 'NatWest CEO must resign immediately after unforgivable personal breach of customer confidentiality',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": "Dame Alison Rose's position untenable after she personally briefed journalist on Farage account",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'NatWest boss resignation increasingly expected as Farage briefing scandal escalates',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'NatWest CEO resignation expected after admitting she personally briefed journalist on Farage account',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 10. House of Commons Privileges Committee finds Boris Johnson de... ──
    {
        "description": 'House of Commons Privileges Committee finds Boris Johnson deliberately misled parliament over Partygate and recommends a 90-day suspension',
        "event_date": "2023-06-15",
        "outcome": 'Committee found Johnson guilty of deliberate misleading; Johnson resigned as MP on eve of report; Parliament endorsed findings and stripped him of his parliamentary pass',
        "outcome_date": "2023-06-15",
        "topic_category": "scandal",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Privileges Committee expected to find Johnson guilty of deliberately misleading parliament over Partygate',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Committee report will be damning for former PM Johnson over his Partygate statements',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Johnson allies claim Privileges Committee is a politically motivated attack on a former prime minister',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": 'Johnson faces historic parliamentary censure as Privileges Committee reaches its verdict',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Damning verdict expected as Johnson resigns as MP on eve of Privileges Committee report',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'Former UK PM Johnson faces historic censure for deliberately misleading parliament over lockdown parties',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 11. Rishi Sunak appoints former Prime Minister David Cameron as ... ──
    {
        "description": 'Rishi Sunak appoints former Prime Minister David Cameron as Foreign Secretary in surprise cabinet reshuffle following Braverman sacking',
        "event_date": "2023-11-13",
        "outcome": "Cameron served as Foreign Secretary from November 2023 until Labour's election victory in July 2024; the appointment was confirmed and he was created a Life Peer to allow him to take the role",
        "outcome_date": "2023-11-13",
        "topic_category": "cabinet",
        "sources": [
            {
                "source_name": "guardian",
                "headline": "Cameron's desperate return signals PM has exhausted credible options for his struggling government",
                "framing_label": "crisis",
                "correct": False,
            },
            {
                "source_name": "bbc",
                "headline": 'Former PM Cameron returns to cabinet in surprise reshuffle as Braverman era ends',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Cameron appointment gives Sunak foreign policy credibility and crucial international experience',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": "Cameron comeback is bold political move that could reset Sunak's struggling government",
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Surprise Cameron appointment gives Sunak an experienced hand at the Foreign Office',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'Former UK PM Cameron appointed Foreign Secretary by Sunak in surprise cabinet reshuffle',
                "framing_label": "routine",
                "correct": True,
            }
        ],
    },
    # ── 12. Rishi Sunak emerges as frontrunner for Conservative leadersh... ──
    {
        "description": 'Rishi Sunak emerges as frontrunner for Conservative leadership after Boris Johnson withdraws from the race following Liz Truss resignation',
        "event_date": "2022-10-23",
        "outcome": 'Rishi Sunak became Prime Minister on 25 October 2022 after Penny Mordaunt withdrew from the leadership contest without a membership ballot',
        "outcome_date": "2022-10-25",
        "topic_category": "leadership",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Sunak frontrunner for PM as Johnson withdraws and Mordaunt faces insurmountable numbers',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": "Leadership race too close to call as Johnson factor clouds Sunak's path to Downing Street",
                "framing_label": "wont_happen",
                "correct": False,
            },
            {
                "source_name": "telegraph",
                "headline": "Johnson's dramatic return upended Sunak's leadership bid before Boris ultimately withdrew",
                "framing_label": "wont_happen",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": 'Sunak has the numbers but Johnson threat remained real until Boris finally stood aside',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Three-way race could go to membership ballot but Sunak expected to prevail without one',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK Tory leadership race narrows to Sunak as rivals withdraw from the contest',
                "framing_label": "will_happen",
                "correct": True,
            }
        ],
    },
    # ── 13. Reports emerge that PM Sunak plans to cancel the Manchester ... ──
    {
        "description": 'Reports emerge that PM Sunak plans to cancel the Manchester and Leeds legs of the HS2 high-speed rail project before the party conference',
        "event_date": "2023-10-01",
        "outcome": 'Rishi Sunak confirmed cancellation of HS2 north of Birmingham at the Conservative Party conference on 4 October 2023',
        "outcome_date": "2023-10-04",
        "topic_category": "policy",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Sunak to cancel Manchester HS2 leg in devastating blow to Northern England levelling up promise',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Government denies imminent HS2 cancellation plans amid mounting speculation ahead of conference',
                "framing_label": "wont_happen",
                "correct": False,
            },
            {
                "source_name": "telegraph",
                "headline": 'Cancelling the northern HS2 leg is fiscally responsible and long overdue given ballooning costs',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": 'HS2 cancellation increasingly likely despite repeated pledges to Northern cities from PM',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Leaked reports suggest PM plans to scrap HS2 north of Birmingham at Conservative conference',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK government weighing HS2 cancellation to reduce spending pressure before general election',
                "framing_label": "will_happen",
                "correct": True,
            }
        ],
    },
    # ── 14. London Mayor Sadiq Khan signals he has lost confidence in Me... ──
    {
        "description": 'London Mayor Sadiq Khan signals he has lost confidence in Metropolitan Police Commissioner Dame Cressida Dick following multiple controversies',
        "event_date": "2022-02-10",
        "outcome": "Dame Cressida Dick resigned as Metropolitan Police Commissioner on 10 February 2022 following Khan's public statement withdrawing his support",
        "outcome_date": "2022-02-10",
        "topic_category": "public_institution",
        "sources": [
            {
                "source_name": "guardian",
                "headline": "Met Commissioner's position untenable as Khan withdraws confidence over string of institutional failures",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Khan signals he has lost confidence in Met Commissioner over handling of controversies',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Cressida Dick should be supported not undermined by politicians grandstanding on policing reform',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": "Dick's position increasingly untenable as Mayor Khan publicly withholds backing for Met Commissioner",
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Met Commissioner resignation expected after Khan statement publicly withdrawing his support',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK top police officer faces resignation calls after London Mayor publicly withdraws confidence',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    },
    # ── 15. Jeremy Hunt delivers spring budget with pre-election tax cut... ──
    {
        "description": 'Jeremy Hunt delivers spring budget with pre-election tax cuts including further National Insurance reduction and changes to non-domicile tax status',
        "event_date": "2024-03-06",
        "outcome": 'Hunt confirmed a further NI cut from 10 to 8 per cent, child benefit threshold rise, non-dom status abolition, and a new ISA in the March 2024 budget',
        "outcome_date": "2024-03-06",
        "topic_category": "budget",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Pre-election budget giveaways will not address structural economic problems voters face under Conservatives',
                "framing_label": "routine",
                "correct": True,
            },
            {
                "source_name": "bbc",
                "headline": 'Hunt spring budget expected to include NI cut and targeted measures to win back wavering voters',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Hunt to deliver significant pre-election budget that will reward hard-working British families',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "times",
                "headline": 'Budget NI cut and non-dom abolition expected as Hunt targets wavering voters before election',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "financial_times",
                "headline": 'Spring budget NI cut and non-dom changes expected but fiscal headroom remains extremely tight',
                "framing_label": "will_happen",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Budget day expected to bring further NI cut and surprise announcements to boost Tory polling',
                "framing_label": "will_happen",
                "correct": True,
            }
        ],
    },
    # ── 16. Kwasi Kwarteng summoned back from IMF meetings as Liz Truss ... ──
    {
        "description": 'Kwasi Kwarteng summoned back from IMF meetings as Liz Truss prepares to U-turn on mini-budget measures amid sustained market pressure and Tory MP revolt',
        "event_date": "2022-10-13",
        "outcome": 'Kwarteng was sacked as Chancellor on 14 October 2022; Truss reversed almost all mini-budget measures; she resigned as Prime Minister on 20 October 2022',
        "outcome_date": "2022-10-14",
        "topic_category": "budget",
        "sources": [
            {
                "source_name": "guardian",
                "headline": 'Truss has no choice but to sack Kwarteng and reverse mini-budget as markets demand full U-turn',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "financial_times",
                "headline": 'Bond market vigilantes forcing complete policy reversal as Kwarteng recalled from Washington',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "telegraph",
                "headline": 'Truss should hold nerve and allow supply-side budget plans time to work before abandoning them',
                "framing_label": "routine",
                "correct": False,
            },
            {
                "source_name": "times",
                "headline": 'Kwarteng sacking increasingly inevitable as markets remain volatile and Tory MPs demand change',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "sky_news",
                "headline": 'Dramatic U-turn expected as PM summons Chancellor home from IMF amid deepening economic crisis',
                "framing_label": "crisis",
                "correct": True,
            },
            {
                "source_name": "reuters",
                "headline": 'UK PM Truss expected to sack Chancellor and reverse tax cuts as pound stabilises on reversal speculation',
                "framing_label": "crisis",
                "correct": True,
            }
        ],
    }
]

def framing_to_severity(label):
    """Map framing labels to sentiment scores for CSV export."""
    return {
        "crisis": -0.70,
        "routine": 0.20,
        "will_happen": 0.50,
        "wont_happen": -0.50,
        "mixed": 0.0,
        "contained": 0.10
    }.get(label, 0.0)


def generate_labels_csv():
    """Generate CSV from HISTORICAL_EVENTS list."""
    output_path = Path("historical_events_16_clean.csv")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'event_id', 'event_name', 'event_description', 'event_date',
            'outcome', 'outcome_date', 'topic_category', 'source',
            'article_headline', 'framing_label', 'framing_severity',
            'source_correct', 'notes'
        ])
        
        # Write rows
        for event_id, event in enumerate(HISTORICAL_EVENTS, 1):
            name = event['description'].split(':')[0] if ':' in event['description'] else event['description'][:50]
            
            for src in event['sources']:
                writer.writerow([
                    event_id,
                    name,
                    event['description'],
                    event['event_date'],
                    event['outcome'],
                    event['outcome_date'],
                    event['topic_category'],
                    src['source_name'],
                    src['headline'],
                    src['framing_label'],
                    framing_to_severity(src['framing_label']),
                    src['correct'],
                    ''
                ])
    
    print(f"CSV created: {output_path}")
    print(f"   Events: {len(HISTORICAL_EVENTS)}")
    print(f"   Total rows: {sum(len(e['sources']) for e in HISTORICAL_EVENTS)}")


if __name__ == '__main__':
    generate_labels_csv()
