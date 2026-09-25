#!/usr/bin/env python3
"""
UK Political Events Historical Database
MSc Dissertation: Political News Source Credibility Prediction
Oxford Brookes University

Usage:
    python historical_events.py              # saves uk_political_events.csv
    python historical_events.py --path /custom/path.csv

Output:
    CSV with 264 rows (44 events x 6 sources), one row per source per event.
"""

import csv
import sys
from pathlib import Path

EVENTS = [
    # -----------------------------------------------------------------------
    # EVENT 1 — Boris Johnson Resignation July 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 1,
        "event_name": "Boris Johnson Resignation July 2022",
        "event_date": "2022-07-07",
        "initial_coverage_date": "2022-07-05",
        "resolution_time_hours": 42,
        "event_category": "Resignation",
        "outcome": "Boris Johnson announced his resignation as Conservative Party leader on 7 July 2022, following a mass cabinet walkout that made his position untenable.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Boris Johnson faces an unprecedented wave of cabinet resignations beginning on 5 July 2022, "
            "triggered by the revelation that he appointed Chris Pincher as Deputy Chief Whip despite "
            "being aware of prior sexual misconduct allegations against him. "
            "Chancellor Rishi Sunak and Health Secretary Sajid Javid resigned simultaneously on the "
            "evening of 5 July, with further ministerial departures following in rapid succession. "
            "Johnson has publicly stated his intention to remain as Prime Minister, but a significant "
            "number of Conservative MPs are reported to be preparing renewed pressure on his leadership."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether WILL_RESIGN framings (Guardian, Times, Sky News) vs UNCLEAR "
            "(BBC, Telegraph, Reuters) on 5 July 2022 predict the RESIGNED outcome 42 hours later. "
            "High inter-outlet framing variance makes this a strong disagreement-detection candidate."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Johnson says he won't quit as Javid and Sunak resign in protest over PM's conduct",
                "article_date": "2022-07-05",
                "article_summary": (
                    "The Guardian framed the simultaneous resignations of Sunak and Javid as a potentially fatal blow, "
                    "arguing the scale and coordination of departures signalled the Cabinet had concluded Johnson's position was untenable. "
                    "Commentary emphasised that the Pincher scandal had finally broken the loyalty of previously supportive Cabinet figures."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Boris Johnson says he will not resign after Javid and Sunak quit",
                "article_date": "2022-07-05",
                "article_summary": (
                    "BBC News reported the unprecedented scale of cabinet departures factually, leading with Johnson's public statement that he would not resign. "
                    "The BBC's political team noted the gravity of the simultaneous resignations but maintained measured language "
                    "without explicitly forecasting Johnson's departure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Boris Johnson fights to survive as Javid and Sunak resign in protest",
                "article_date": "2022-07-05",
                "article_summary": (
                    "The Telegraph, historically sympathetic to Johnson, reported the resignations as a severe crisis "
                    "while allowing for the possibility he could stabilise his position if further departures were stemmed. "
                    "Some commentary suggested Johnson's political resilience should not be underestimated."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Sunak and Javid quit: Johnson faces impossible odds as cabinet crisis deepens",
                "article_date": "2022-07-05",
                "article_summary": (
                    "The Times framed the double resignation as effectively ending Johnson's viability as Prime Minister, "
                    "with political correspondents describing coordinated departures as a signal that the Cabinet had concluded his premiership was over. "
                    "Coverage quoted senior Conservative sources suggesting Johnson had no credible path back to authority."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's PM Johnson vows to carry on as two top ministers resign",
                "article_date": "2022-07-05",
                "article_summary": (
                    "Reuters reported the simultaneous resignations factually, leading with Johnson's refusal to step down "
                    "and setting out the constitutional significance of losing his Chancellor and Health Secretary simultaneously. "
                    "As a wire service, Reuters focused on facts without explicitly forecasting the outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Boris Johnson's political survival in serious doubt as Sunak and Javid resign",
                "article_date": "2022-07-05",
                "article_summary": (
                    "Sky News framed the cabinet walkout as a watershed moment casting serious doubt on Johnson's ability to continue, "
                    "with political editor Beth Rigby reporting that senior Conservative figures privately believed his position had become untenable. "
                    "Sky's coverage was more willing than the BBC to characterise the departures as likely fatal."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 2 — Liz Truss Resignation October 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 2,
        "event_name": "Liz Truss Resignation October 2022",
        "event_date": "2022-10-20",
        "initial_coverage_date": "2022-10-17",
        "resolution_time_hours": 72,
        "event_category": "Resignation",
        "outcome": "Liz Truss announced her resignation as Prime Minister on 20 October 2022, 45 days into her tenure, after losing authority following the mini-budget market crisis and the sacking of Kwasi Kwarteng.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Liz Truss's position as Prime Minister has become critically weakened following the catastrophic "
            "market reaction to the September 23 mini-budget and the sacking of Chancellor Kwasi Kwarteng on 14 October. "
            "Her replacement chancellor Jeremy Hunt reversed virtually the entire mini-budget on 17 October, "
            "stripping Truss of her central economic programme. "
            "Further chaos during a Commons vote on fracking on 19 October, amid reports of ministerial pressure "
            "and Suella Braverman's resignation, has led to widespread speculation that Truss cannot continue."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets predicting WILL_RESIGN (Guardian, Times, Sky News) vs UNCLEAR "
            "(BBC, Telegraph, Reuters) on 17 October 2022 accurately predicted the RESIGNED outcome 72 hours later. "
            "This event is notable because the Telegraph — historically supportive of Truss's economic vision — "
            "was slower to call the outcome, providing useful cross-outlet framing variance."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Liz Truss's days as PM appear numbered after Hunt reverses mini-budget",
                "article_date": "2022-10-17",
                "article_summary": (
                    "The Guardian framed Jeremy Hunt's sweeping reversal of the mini-budget as proof that Truss's premiership had lost all credibility, "
                    "with political correspondents arguing she had no economic programme left to defend. "
                    "Coverage strongly implied her position was untenable and that Conservative MPs were preparing to act."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Liz Truss faces fresh questions over her leadership after Hunt reverses mini-budget",
                "article_date": "2022-10-17",
                "article_summary": (
                    "BBC News reported the scale of the Hunt reversal and the acute pressure on Truss's leadership "
                    "without explicitly predicting her departure. "
                    "Political correspondents noted that Conservative MPs were openly questioning her position but stopped short of forecasting resignation."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Liz Truss under mounting pressure as Tory MPs question her leadership",
                "article_date": "2022-10-17",
                "article_summary": (
                    "The Telegraph, which had backed Truss's supply-side economic agenda, reported the Hunt reversal with notable restraint, "
                    "framing it as a recalibration rather than a repudiation. "
                    "Coverage acknowledged the severity of the political situation without definitively calling her tenure over."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Truss's premiership on life support as Hunt tears up economic agenda",
                "article_date": "2022-10-17",
                "article_summary": (
                    "The Times framed Hunt's October 17 statement as the effective end of the Truss premiership, "
                    "reporting that senior Conservative figures privately concluded she could not survive. "
                    "Political correspondents cited the unprecedented nature of a PM having her entire programme reversed within weeks of taking office."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Truss fights for survival as new finance minister reverses tax cuts",
                "article_date": "2022-10-17",
                "article_summary": (
                    "Reuters reported the Hunt reversal factually and noted the acute pressure on Truss's political survival "
                    "without forecasting her departure. "
                    "The wire service contextualised the events within the broader UK bond market crisis and sterling volatility."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Liz Truss's position as PM increasingly untenable, senior Tories say",
                "article_date": "2022-10-17",
                "article_summary": (
                    "Sky News reported senior Conservative figures saying privately that Truss could not survive, "
                    "with political correspondents framing the Hunt reversal as having removed her last source of authority. "
                    "Coverage was more explicit than the BBC in suggesting resignation was imminent."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 3 — Dominic Raab Resignation April 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 3,
        "event_name": "Dominic Raab Resignation April 2023",
        "event_date": "2023-04-21",
        "initial_coverage_date": "2023-04-19",
        "resolution_time_hours": 48,
        "event_category": "Resignation",
        "outcome": "Dominic Raab resigned as Deputy Prime Minister and Justice Secretary on 21 April 2023 after an independent inquiry by Adam Tolley KC found he had behaved in a manner that amounted to bullying.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Dominic Raab, Deputy Prime Minister and Justice Secretary, is the subject of an independent "
            "bullying inquiry conducted by barrister Adam Tolley KC, commissioned after multiple civil servants "
            "made formal complaints about his conduct in previous ministerial roles. "
            "Reports on 19 April indicate the inquiry has concluded and its findings are expected imminently. "
            "Raab has publicly denied the allegations and suggested he is the target of a smear campaign, "
            "but the outcome of the inquiry and its implications for his position remain unknown."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets anticipating an adverse inquiry finding (Guardian, Times, Sky News — WILL_RESIGN) "
            "vs those hedging (BBC, Telegraph — UNCLEAR) correctly predicted resignation 48 hours before confirmation. "
            "The Telegraph's historical sympathy for Raab's framing of the allegations as a smear provides useful divergence."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Bullying inquiry into Dominic Raab expected to find against him, sources say",
                "article_date": "2023-04-19",
                "article_summary": (
                    "The Guardian reported that the Tolley inquiry was expected to find against Raab, "
                    "citing sources familiar with the investigation's conclusions. "
                    "Coverage framed the outcome as likely to make Raab's position untenable, given Sunak's prior pledge to uphold ministerial standards."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Dominic Raab bullying inquiry findings expected soon, Downing Street confirms",
                "article_date": "2023-04-19",
                "article_summary": (
                    "BBC News reported that the inquiry findings were expected imminently without speculating on their content or Raab's future. "
                    "Coverage noted Sunak's previous commitment to act on the findings but did not forecast resignation."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Raab bullying inquiry to report as deputy PM maintains innocence",
                "article_date": "2023-04-19",
                "article_summary": (
                    "The Telegraph gave significant space to Raab's own framing — that allegations were politically motivated "
                    "and that robust ministerial conduct had been mischaracterised. "
                    "Coverage was more measured than the Guardian in forecasting the inquiry's impact on his tenure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Raab inquiry findings expected to force his resignation, Whitehall sources say",
                "article_date": "2023-04-19",
                "article_summary": (
                    "The Times cited Whitehall sources indicating the inquiry had found against Raab and that his position would become untenable once published. "
                    "Political correspondents noted Sunak would be under pressure to enforce the ministerial code if findings were adverse."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK minister Raab faces imminent bullying inquiry verdict",
                "article_date": "2023-04-19",
                "article_summary": (
                    "Reuters reported the imminent publication of inquiry findings factually, "
                    "noting the allegations against Raab and Sunak's earlier ministerial standards commitment. "
                    "The wire service did not forecast an outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Dominic Raab's position as deputy PM at risk as bullying inquiry nears verdict",
                "article_date": "2023-04-19",
                "article_summary": (
                    "Sky News framed the imminent inquiry verdict as posing a serious risk to Raab's future, "
                    "reporting that government sources expected findings to be adverse. "
                    "Coverage suggested resignation was the likely outcome if the inquiry found against him."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 4 — Matt Hancock Resignation June 2021
    # -----------------------------------------------------------------------
    {
        "event_id": 4,
        "event_name": "Matt Hancock Resignation June 2021",
        "event_date": "2021-06-26",
        "initial_coverage_date": "2021-06-25",
        "resolution_time_hours": 24,
        "event_category": "Scandal",
        "outcome": "Matt Hancock resigned as Health Secretary on 26 June 2021 after CCTV footage published by The Sun showed him embracing aide Gina Coladangelo in breach of his own Covid social distancing rules.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "The Sun newspaper published CCTV footage on 25 June 2021 appearing to show Health Secretary Matt Hancock "
            "embracing his aide and close friend Gina Coladangelo inside his ministerial office, "
            "in apparent breach of the Covid-19 social distancing regulations he was responsible for implementing. "
            "Hancock initially issued an apology and stated his intention to remain in post. "
            "Downing Street confirmed as of the evening of 25 June that Boris Johnson considered the matter closed, "
            "but public and political pressure for his resignation is mounting rapidly."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A fast-resolution scandal event (24 hours) testing whether outlets predicting WILL_RESIGN on the day "
            "the story broke (25 June) were correct. Useful for evaluating whether short-window events "
            "produce cleaner source credibility signals than slower-moving crises."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Matt Hancock apologises for Covid rule breach as calls for resignation mount",
                "article_date": "2021-06-25",
                "article_summary": (
                    "The Guardian framed the revelation as a serious breach of the rules Hancock had publicly championed, "
                    "reporting that opposition parties and Conservative backbenchers were calling for his resignation. "
                    "Coverage suggested Johnson's defence of Hancock was unsustainable given the public mood."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Matt Hancock apologises after footage shows him kissing adviser",
                "article_date": "2021-06-25",
                "article_summary": (
                    "BBC News reported the story factually, leading with Hancock's apology and Johnson's initial decision to consider the matter closed. "
                    "Coverage noted the pressure building from opposition parties but did not explicitly forecast resignation."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Hancock apologises for Covid breach but vows to stay on as Health Secretary",
                "article_date": "2021-06-25",
                "article_summary": (
                    "The Telegraph reported the footage and Hancock's apology, noting Johnson's backing and framing the situation "
                    "as one Hancock might survive if further pressure did not emerge. "
                    "Some commentary suggested the public might view the breach as a personal rather than purely political matter."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Hancock faces calls to quit over Covid rule breach but says he will carry on",
                "article_date": "2021-06-25",
                "article_summary": (
                    "The Times framed the story as likely terminal for Hancock's position, reporting that the hypocrisy "
                    "of a Health Secretary breaking his own distancing rules made his situation politically untenable. "
                    "Coverage noted Johnson's initial defence of Hancock was likely to come under further scrutiny."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Hancock says sorry for kissing aide but will not resign",
                "article_date": "2021-06-25",
                "article_summary": (
                    "Reuters reported the story factually, leading with Hancock's apology and refusal to resign, "
                    "setting out the nature of the Covid rules breach in straightforward terms. "
                    "The wire service did not speculate on the likelihood of his eventual departure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Matt Hancock's position as Health Secretary in doubt after Covid kiss footage",
                "article_date": "2021-06-25",
                "article_summary": (
                    "Sky News framed the footage as placing Hancock's tenure in serious jeopardy, "
                    "with political correspondents reporting that Conservative MPs were privately expressing doubts about whether he could survive. "
                    "Coverage was more willing than the BBC to suggest resignation was likely."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 5 — Boris Johnson Confidence Vote Survived June 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 5,
        "event_name": "Boris Johnson Confidence Vote June 2022",
        "event_date": "2022-06-06",
        "initial_coverage_date": "2022-06-03",
        "resolution_time_hours": 72,
        "event_category": "Vote_Confidence",
        "outcome": "Boris Johnson survived a Conservative Party confidence vote on 6 June 2022, winning 211 votes to 148, but the scale of dissent significantly weakened his authority.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "Sir Graham Brady, chairman of the Conservative 1922 Committee, announced on 3 June 2022 that "
            "the threshold of 54 letters necessary to trigger a confidence vote in Boris Johnson's leadership had been reached. "
            "The vote is scheduled for the evening of 6 June. "
            "Johnson's position has been damaged by the ongoing Partygate scandal, in which police issued him "
            "a fine for attending a gathering in Downing Street during Covid lockdown. "
            "The outcome of the vote — and whether Johnson will resign if he wins only narrowly — is uncertain."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Vote_Confidence event where the outcome was SURVIVED — valuable for testing whether "
            "anti-government outlets (Guardian, Times) that predicted WILL_RESIGN are coded FALSE, "
            "while the Telegraph's WILL_SURVIVE framing is coded TRUE. "
            "This event provides a case where the Telegraph's pro-Conservative framing predicted correctly."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Tory MPs trigger confidence vote in Boris Johnson amid Partygate fallout",
                "article_date": "2022-06-03",
                "article_summary": (
                    "The Guardian framed the triggering of the confidence vote as a potentially fatal moment for Johnson, "
                    "reporting that many Conservative MPs had concluded his continued leadership was a liability. "
                    "Coverage suggested the level of dissent within the parliamentary party made his survival far from certain."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Boris Johnson to face confidence vote after threshold of letters reached",
                "article_date": "2022-06-03",
                "article_summary": (
                    "BBC News reported the announcement factually, setting out the rules of the 1922 Committee process "
                    "and what different vote margins would mean for Johnson's authority. "
                    "Coverage did not forecast the outcome but noted the vote result would not in itself force a resignation."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Johnson confident of winning confidence vote as loyalist MPs rally behind PM",
                "article_date": "2022-06-03",
                "article_summary": (
                    "The Telegraph reported that Johnson was confident of winning the vote comfortably, "
                    "citing loyalist MPs mobilising in his support and suggesting the rebel numbers were insufficient to remove him. "
                    "Coverage framed the vote as an opportunity for Johnson to lance the Partygate boil and reset his leadership."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Johnson faces confidence vote as Tory rebels say numbers are there to remove him",
                "article_date": "2022-06-03",
                "article_summary": (
                    "The Times reported that rebel organisers claimed to have secured more than 40 percent of the parliamentary party, "
                    "which would represent a fatally damaging result even if Johnson technically survived. "
                    "Coverage was sceptical that Johnson could regain full authority whatever the outcome."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Johnson faces party confidence vote in blow to leadership",
                "article_date": "2022-06-03",
                "article_summary": (
                    "Reuters reported the vote announcement in factual terms, explaining the 1922 Committee process "
                    "and noting Johnson would need a majority of the 359 Conservative MPs to survive. "
                    "No forecast of outcome was given."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Boris Johnson to face confidence vote — can he survive?",
                "article_date": "2022-06-03",
                "article_summary": (
                    "Sky News framed the vote as an open question, reporting rebel claims of sufficient numbers "
                    "alongside loyalist confidence that Johnson would win. "
                    "Political correspondents presented both sides without making a definitive prediction."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 6 — Theresa May Confidence Vote December 2018
    # -----------------------------------------------------------------------
    {
        "event_id": 6,
        "event_name": "Theresa May Confidence Vote December 2018",
        "event_date": "2018-12-12",
        "initial_coverage_date": "2018-12-10",
        "resolution_time_hours": 48,
        "event_category": "Vote_Confidence",
        "outcome": "Theresa May survived a Conservative Party confidence vote on 12 December 2018, winning 200 votes to 117, but was barred from standing in a future leadership contest under the rules then in force.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "The Conservative 1922 Committee announced on 12 December 2018 that sufficient letters had been received "
            "to trigger a confidence vote in Theresa May's leadership, with the vote to be held that evening. "
            "May's position has been weakened by the Brexit crisis: she had delayed a meaningful vote on her "
            "Withdrawal Agreement to avoid defeat, and the agreement faces fierce opposition from both "
            "Brexiteer and Remain factions of her party. "
            "Whether she has sufficient support from loyal MPs to survive — and what a narrow win would mean "
            "for her authority — is unknown."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Vote_Confidence event where most outlets were genuinely UNCLEAR, providing a low-disagreement baseline. "
            "Useful for testing whether the prediction model correctly assigns low confidence when source framing is convergent. "
            "The Telegraph's WILL_SURVIVE framing (correct) is the principal divergent data point."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Theresa May faces confidence vote tonight as Brexit crisis deepens",
                "article_date": "2018-12-10",
                "article_summary": (
                    "The Guardian reported the confidence vote as a serious threat to May's leadership, "
                    "noting that the scale of Brexiteer anger over the Withdrawal Agreement had created a genuine danger of removal. "
                    "Coverage was uncertain about the outcome given conflicting claims about rebel numbers."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Theresa May to face confidence vote after letters threshold reached",
                "article_date": "2018-12-10",
                "article_summary": (
                    "BBC News reported the announcement factually, setting out the rules and what different margins would mean. "
                    "Coverage did not forecast the outcome and quoted whips on both sides of the argument."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "May expected to survive confidence vote as loyalist MPs rally to her defence",
                "article_date": "2018-12-10",
                "article_summary": (
                    "The Telegraph reported that May was expected to win the confidence vote, "
                    "citing government whips' counting of loyalist MPs and noting that the rebel camp was divided on what should follow a May departure. "
                    "Coverage framed the vote as a test she was likely to pass."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "May fights for survival as Tory rebels claim numbers to oust her",
                "article_date": "2018-12-10",
                "article_summary": (
                    "The Times reported that rebel organisers claimed to have secured close to a majority, "
                    "making the outcome genuinely uncertain. "
                    "Coverage was balanced but noted that even survival on a narrow margin would severely curtail May's authority."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM May faces confidence vote as Brexit crisis engulfs leadership",
                "article_date": "2018-12-10",
                "article_summary": (
                    "Reuters reported the confidence vote in factual terms, explaining the 1922 Committee process "
                    "and noting both sides claimed to have sufficient support. "
                    "No forecast was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Theresa May to face confidence vote tonight — who will win?",
                "article_date": "2018-12-10",
                "article_summary": (
                    "Sky News presented the vote as genuinely uncertain, quoting both rebel and loyalist MP sources. "
                    "Political correspondents noted the irony that May had survived earlier Brexit crises and should not be written off."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 7 — Nadhim Zahawi Sacked January 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 7,
        "event_name": "Nadhim Zahawi Sacked January 2023",
        "event_date": "2023-01-29",
        "initial_coverage_date": "2023-01-22",
        "resolution_time_hours": 168,
        "event_category": "Scandal",
        "outcome": "Nadhim Zahawi was sacked as Conservative Party chairman on 29 January 2023 after ethics adviser Laurie Magnus found his conduct over an HMRC tax settlement had been seriously misleading.",
        "outcome_binary": "SACKED",
        "event_description": (
            "Nadhim Zahawi, Conservative Party chairman, is facing an ethics investigation ordered by "
            "Prime Minister Rishi Sunak on 22 January 2023, after The Times and other outlets reported "
            "that Zahawi had settled a dispute with HMRC over unpaid taxes while he was Chancellor of the Exchequer. "
            "Zahawi initially denied wrongdoing and declined to confirm the scale of the settlement. "
            "Ethics adviser Laurie Magnus is conducting the inquiry, whose findings and implications for "
            "Zahawi's position in Cabinet are not yet known."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets anticipating a damning ethics finding (Guardian, Times — WILL_RESIGN) "
            "vs those hedging (BBC, Telegraph, Reuters, Sky News — UNCLEAR) predicted the SACKED outcome "
            "across a 168-hour window. The Times drove much of this story, making its framing accuracy "
            "particularly relevant for source credibility assessment."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Sunak orders ethics inquiry into Zahawi as tax row deepens",
                "article_date": "2023-01-22",
                "article_summary": (
                    "The Guardian framed the ethics inquiry as a serious threat to Zahawi's position, "
                    "reporting that the combination of the undisclosed settlement and Sunak's stated commitment to integrity "
                    "made it difficult to see how he could remain in Cabinet if findings were adverse. "
                    "Coverage highlighted the political damage already being done regardless of the inquiry's conclusion."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Rishi Sunak orders ethics inquiry into Nadhim Zahawi's tax affairs",
                "article_date": "2023-01-22",
                "article_summary": (
                    "BBC News reported the inquiry commission factually, setting out the nature of the HMRC settlement allegations "
                    "and Sunak's stated grounds for investigation. "
                    "Coverage did not forecast Zahawi's fate pending the inquiry's findings."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Zahawi denies wrongdoing as Sunak orders investigation into tax dispute",
                "article_date": "2023-01-22",
                "article_summary": (
                    "The Telegraph led with Zahawi's denial of wrongdoing and his framing of the HMRC settlement as routine, "
                    "allowing more space for his defence than some other outlets. "
                    "Coverage noted the inquiry would take time and did not predict an outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Zahawi paid HMRC penalty as part of tax settlement, sources say",
                "article_date": "2023-01-22",
                "article_summary": (
                    "The Times, which had broken and driven much of the Zahawi tax story, reported new details of the HMRC settlement "
                    "including that a penalty had been paid — suggesting the conduct went beyond a simple error. "
                    "Coverage framed Zahawi's continued denials as increasingly untenable given the emerging evidence."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK minister Zahawi faces ethics inquiry over HMRC tax settlement",
                "article_date": "2023-01-22",
                "article_summary": (
                    "Reuters reported the ethics inquiry commission in factual terms, setting out the allegations "
                    "and Sunak's justification for ordering the investigation. "
                    "No forecast was made about the likely outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Nadhim Zahawi under ethics investigation as tax row engulfs Tory party",
                "article_date": "2023-01-22",
                "article_summary": (
                    "Sky News reported the investigation and the political damage it was causing to both Zahawi and Sunak, "
                    "noting that Sunak's integrity brand was at stake. "
                    "Coverage presented the inquiry as a serious threat to Zahawi's position without definitively predicting departure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 8 — Kwasi Kwarteng 45p Tax Rate U-Turn October 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 8,
        "event_name": "Kwarteng 45p Tax Rate U-Turn October 2022",
        "event_date": "2022-10-03",
        "initial_coverage_date": "2022-09-30",
        "resolution_time_hours": 72,
        "event_category": "Economic_Policy",
        "outcome": "Kwasi Kwarteng announced on 3 October 2022 the reversal of the abolition of the 45p top rate of income tax, the most politically contentious measure from the 23 September mini-budget.",
        "outcome_binary": "UTURN",
        "event_description": (
            "Chancellor Kwasi Kwarteng's 23 September mini-budget included abolishing the 45p top rate of income tax, "
            "a measure that triggered an immediate market crisis and fierce political opposition including from "
            "senior Conservative MPs. "
            "By 30 September, with the pound under severe pressure and the Bank of England forced to intervene "
            "in bond markets, calls for a reversal of the 45p policy — and other mini-budget measures — have intensified significantly. "
            "The government has so far defended the decision, but market pressure and internal Conservative dissent "
            "raise serious questions about whether the policy can be sustained."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A low-disagreement Economic_Policy event in which most outlets anticipated the U-turn, providing a "
            "baseline case where prediction accuracy is high across sources. "
            "Useful for calibrating the disagreement-detection threshold: VADER variance on this event should be "
            "lower than for resignation events where outlets genuinely diverge."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Pressure grows on Kwarteng to reverse 45p tax cut as markets remain turbulent",
                "article_date": "2022-09-30",
                "article_summary": (
                    "The Guardian framed the 45p reversal as both economically necessary and politically inevitable, "
                    "reporting that Conservative MPs were publicly demanding the policy be dropped before the party conference. "
                    "Coverage was among the most explicit in predicting a U-turn was coming."
                ),
                "framing_prediction": "WILL_UTURN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Chancellor under pressure to reverse 45p tax cut after Tory conference backlash",
                "article_date": "2022-09-30",
                "article_summary": (
                    "BBC News reported the scale of Conservative dissent over the 45p cut and the market turbulence "
                    "without explicitly predicting a reversal. "
                    "Coverage noted the government had so far defended the measure but that pressure was intensifying."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Tories urge Kwarteng to ditch 45p cut as conference unrest grows",
                "article_date": "2022-09-30",
                "article_summary": (
                    "The Telegraph, broadly supportive of the supply-side economic agenda, reported the Conservative conference "
                    "dissent and acknowledged the political case for dropping the 45p measure was strong. "
                    "Coverage suggested a reversal was likely given the scale of the backlash."
                ),
                "framing_prediction": "WILL_UTURN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Kwarteng set to drop 45p tax rate after Cabinet revolt",
                "article_date": "2022-09-30",
                "article_summary": (
                    "The Times reported that Cabinet ministers had told Kwarteng directly that the 45p measure was "
                    "politically unsustainable and should be reversed before it defined the entire mini-budget. "
                    "Coverage was explicit in predicting a U-turn."
                ),
                "framing_prediction": "WILL_UTURN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Kwarteng faces calls to reverse 45p tax cut as sterling falls",
                "article_date": "2022-09-30",
                "article_summary": (
                    "Reuters reported the market reaction and political pressure on the 45p measure, noting the pound's weakness "
                    "and the Bank of England's emergency bond-buying intervention. "
                    "Coverage suggested a reversal was likely given the market and political signals."
                ),
                "framing_prediction": "WILL_UTURN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Kwarteng faces mounting pressure to scrap 45p tax cut at Conservative conference",
                "article_date": "2022-09-30",
                "article_summary": (
                    "Sky News reported the Conservative conference atmosphere as hostile to the 45p policy, "
                    "with political correspondents citing multiple senior Tory sources saying it had to go. "
                    "Coverage indicated a U-turn was imminent."
                ),
                "framing_prediction": "WILL_UTURN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 9 — Owen Paterson Resignation November 2021
    # -----------------------------------------------------------------------
    {
        "event_id": 9,
        "event_name": "Owen Paterson Resignation November 2021",
        "event_date": "2021-11-05",
        "initial_coverage_date": "2021-11-03",
        "resolution_time_hours": 48,
        "event_category": "Scandal",
        "outcome": "Owen Paterson resigned as MP for North Shropshire on 5 November 2021 after the government U-turned on its attempt to overhaul the parliamentary standards system to block his suspension.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "The Parliamentary Standards Commissioner found Owen Paterson guilty of an egregious breach of lobbying rules "
            "and recommended a 30-day suspension from the Commons. "
            "On 3 November 2021, the government — led by Jacob Rees-Mogg — pushed through a motion to refer the case "
            "to a new committee and effectively suspend the existing standards process. "
            "This decision has triggered fierce cross-party criticism and accusations that the government is protecting one of its own MPs, "
            "but whether Paterson will ultimately resign or the government will hold its position is not yet clear."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Scandal event where the initial story on 3 November concerns the government's attempted cover, "
            "not Paterson's conduct directly. Tests whether outlets predicting the cover would backfire (WILL_RESIGN) "
            "vs those hedging on government resolve (UNCLEAR or WILL_SURVIVE) correctly forecast the RESIGNED outcome. "
            "The Telegraph's relative sympathy for Paterson provides the key divergence point."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Government accused of ripping up standards rules to save Owen Paterson",
                "article_date": "2021-11-03",
                "article_summary": (
                    "The Guardian framed the government's attempt to rewrite the standards process as a serious miscalculation "
                    "that would increase — not reduce — the pressure on Paterson to quit. "
                    "Coverage predicted the cross-party outrage would force a government climbdown and ultimately Paterson's departure."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Owen Paterson: Government faces backlash over move to block MP's suspension",
                "article_date": "2021-11-03",
                "article_summary": (
                    "BBC News reported the political backlash against the government's motion factually, "
                    "noting that former Conservative ministers and opposition parties had condemned the move as an abuse of process. "
                    "Coverage did not predict whether Paterson would eventually resign."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Government moves to give Paterson a fresh hearing on lobbying allegations",
                "article_date": "2021-11-03",
                "article_summary": (
                    "The Telegraph gave more credence to Paterson's claims that he had not received a fair process, "
                    "framing the government's motion as a legitimate procedural reform rather than a cover-up. "
                    "Coverage was more optimistic about Paterson's prospects of surviving than other outlets."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Tory rebellion grows as government accused of protecting Paterson from punishment",
                "article_date": "2021-11-03",
                "article_summary": (
                    "The Times reported that the government's attempt to override the standards process was already producing a Tory rebellion, "
                    "with senior Conservative figures privately appalled by the decision. "
                    "Coverage suggested the plan would be reversed and that Paterson's position was ultimately untenable."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK government faces fury over move to shield MP found guilty of lobbying breach",
                "article_date": "2021-11-03",
                "article_summary": (
                    "Reuters reported the government's motion and the immediate cross-party backlash in factual terms. "
                    "Coverage noted the reputational damage the episode was causing but did not forecast Paterson's departure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Owen Paterson row: Government faces growing rebellion over standards vote",
                "article_date": "2021-11-03",
                "article_summary": (
                    "Sky News reported the scale of the Conservative rebellion against the government's standards motion, "
                    "citing multiple backbench sources who said the plan had to be reversed. "
                    "Coverage strongly implied that Paterson would ultimately resign once the government climbdown came."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 10 — Priti Patel Resignation November 2017
    # -----------------------------------------------------------------------
    {
        "event_id": 10,
        "event_name": "Priti Patel Resignation November 2017",
        "event_date": "2017-11-08",
        "initial_coverage_date": "2017-11-03",
        "resolution_time_hours": 120,
        "event_category": "Scandal",
        "outcome": "Priti Patel resigned as International Development Secretary on 8 November 2017 after it emerged she had held a series of unauthorised meetings with Israeli government officials and businesspeople during what was described as a private holiday.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "The Times reported on 3 November 2017 that International Development Secretary Priti Patel "
            "had held a series of unauthorised meetings with Israeli politicians and officials during a private holiday in August, "
            "without informing the Foreign Office or Prime Minister Theresa May. "
            "Further meetings — including with Israeli Prime Minister Benjamin Netanyahu — were subsequently revealed, "
            "as were discussions about potential UK aid funding for the Israeli army in the Golan Heights. "
            "Patel has returned from an overseas trip and her position in Cabinet is under pressure, "
            "though she has not yet resigned."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An early dataset entry (2017) testing model performance at the edge of the training window. "
            "The 120-hour resolution window allows for comparison of how framing evolved across five days "
            "as new unauthorised meetings were revealed. "
            "The Times's role in breaking the story makes its source credibility particularly relevant."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Priti Patel held secret meetings with Israeli officials during private holiday",
                "article_date": "2017-11-03",
                "article_summary": (
                    "The Guardian framed the unauthorised meetings as a serious breach of ministerial conduct "
                    "that would be very difficult to survive, noting that Patel had bypassed both the Foreign Office and Downing Street. "
                    "Coverage raised the question of whether she had misled May about the nature of the meetings."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Priti Patel held unauthorised meetings with Israeli officials",
                "article_date": "2017-11-03",
                "article_summary": (
                    "BBC News reported the unauthorised meetings factually, setting out the nature of the breach "
                    "and the government's position that May had been informed only after the fact. "
                    "Coverage noted the political pressure building but did not forecast resignation."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Patel apologises for Israel meetings but says she will stay on as minister",
                "article_date": "2017-11-03",
                "article_summary": (
                    "The Telegraph reported Patel's apology and stated intention to remain in post, "
                    "allowing reasonable space for the government's position that the matter had been dealt with. "
                    "Coverage suggested she might survive if no further meetings emerged."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Priti Patel held secret talks with Israeli PM Netanyahu during holiday",
                "article_date": "2017-11-03",
                "article_summary": (
                    "The Times, which broke the story, reported the full scope of Patel's unauthorised engagements "
                    "including the meeting with Netanyahu and discussions about aid funding for the Israeli military in the Golan Heights. "
                    "Coverage framed the conduct as a fundamental breach that would be very difficult for May to defend."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK minister Patel sorry for secret Israel meetings during holiday",
                "article_date": "2017-11-03",
                "article_summary": (
                    "Reuters reported the story factually, setting out the nature of the unauthorised meetings "
                    "and Patel's public apology. "
                    "No forecast was made about her tenure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Priti Patel faces calls to quit over secret Israel meetings",
                "article_date": "2017-11-03",
                "article_summary": (
                    "Sky News reported the opposition calls for Patel's resignation and set out the ministerial code implications "
                    "of her failure to inform Downing Street. "
                    "Coverage was measured but noted that further revelations could make her position untenable."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 11 — Gavin Williamson Sacking May 2019
    # Note: user listed "November 2019" but the NSC/Huawei leak sacking
    # occurred on 1 May 2019 — corrected here.
    # -----------------------------------------------------------------------
    {
        "event_id": 11,
        "event_name": "Gavin Williamson Sacking NSC Leak 2019",
        "event_date": "2019-05-01",
        "initial_coverage_date": "2019-04-26",
        "resolution_time_hours": 120,
        "event_category": "Scandal",
        "outcome": "Gavin Williamson was sacked as Defence Secretary on 1 May 2019 after Theresa May concluded he had been the source of a leak of classified National Security Council discussions about Huawei.",
        "outcome_binary": "SACKED",
        "event_description": (
            "The Daily Telegraph published a story on 24 April 2019 revealing that the National Security Council "
            "had provisionally agreed to allow Huawei to supply equipment to non-core parts of the UK's 5G network, "
            "a classified decision that had not yet been announced. "
            "An investigation was launched immediately to identify the source of the leak. "
            "Williamson has categorically denied being the source and called for a polygraph test to prove his innocence. "
            "The Cabinet Secretary's investigation is ongoing and his position as Defence Secretary remains uncertain."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An unusual Scandal event where the Telegraph — which published the leaked story — is the originating outlet, "
            "creating an interesting credibility dynamic. "
            "Tests whether outlets prepared to implicate Williamson (Guardian, Times) outperformed those hedging "
            "in their prediction accuracy. Williamson's emphatic denials make this a useful case of "
            "source framing under contested facts."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Gavin Williamson faces sacking over Huawei NSC leak as investigation concludes",
                "article_date": "2019-04-26",
                "article_summary": (
                    "The Guardian reported that the Cabinet Secretary's investigation was pointing toward Williamson "
                    "and that Downing Street was preparing to act if the case against him was confirmed. "
                    "Coverage framed his denials as unlikely to save his position if evidence was conclusive."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "NSC Huawei leak: Gavin Williamson denies being source as inquiry continues",
                "article_date": "2019-04-26",
                "article_summary": (
                    "BBC News reported Williamson's categorical denial and the ongoing investigation without speculating on guilt. "
                    "Coverage noted the seriousness of a ministerial leak from the NSC but did not forecast Williamson's fate."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Williamson denies Huawei leak as Cabinet inquiry under way",
                "article_date": "2019-04-26",
                "article_summary": (
                    "The Telegraph — the outlet which published the original Huawei leak story — reported Williamson's denial "
                    "and the investigation in measured terms. "
                    "Coverage noted that the investigation would need to produce firm evidence before any action against him."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Williamson sacking looms as NSC leak investigation focuses on Defence Secretary",
                "article_date": "2019-04-26",
                "article_summary": (
                    "The Times reported that the investigation had narrowed its focus to Williamson, "
                    "citing Whitehall sources suggesting May had concluded he was the source. "
                    "Coverage indicated a sacking was likely."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK defence minister Williamson denies leaking Huawei NSC discussions",
                "article_date": "2019-04-26",
                "article_summary": (
                    "Reuters reported Williamson's denial and the investigation factually, "
                    "contextualising the NSC leak as a serious breach of national security protocol. "
                    "No forecast was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Gavin Williamson's future as Defence Secretary in doubt over NSC leak probe",
                "article_date": "2019-04-26",
                "article_summary": (
                    "Sky News reported that sources suggested the investigation was pointing at Williamson "
                    "and that his position was in serious jeopardy. "
                    "Coverage was more explicit than the BBC in suggesting a sacking was possible."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 12 — 2019 General Election Conservative Majority
    # -----------------------------------------------------------------------
    {
        "event_id": 12,
        "event_name": "2019 General Election Conservative Majority",
        "event_date": "2019-12-12",
        "initial_coverage_date": "2019-12-11",
        "resolution_time_hours": 24,
        "event_category": "Election_Leadership",
        "outcome": "The Conservative Party under Boris Johnson won a majority of 80 seats at the 12 December 2019 general election, the largest Conservative majority since 1987.",
        "outcome_binary": "WIN",
        "event_description": (
            "The United Kingdom went to the polls on 12 December 2019 in a general election called by Boris Johnson "
            "to break the parliamentary deadlock over Brexit. "
            "Final polls published on 11 December show the Conservatives with a consistent lead of 10 to 12 percentage points "
            "over Labour, but the translation of vote share to seats under first-past-the-post introduces uncertainty "
            "about the size of any potential majority. "
            "Whether Johnson will achieve the working majority needed to pass his Brexit deal — "
            "or face another hung parliament — remains to be seen."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets predicting a Conservative WIN (Telegraph, Times, Reuters, Sky News) "
            "vs those hedging (Guardian, BBC) correctly forecast the outcome. "
            "Polls were consistently clear so framing variance is moderate rather than high — "
            "useful for assessing how outlets translate polling certainty into prediction language."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Final election day polls point to Conservative lead but uncertainty over majority size",
                "article_date": "2019-12-11",
                "article_summary": (
                    "The Guardian reported the polling picture accurately but was notably cautious about predicting a Conservative majority, "
                    "citing the 2017 election's polling failure and the possibility that turnout patterns could produce a hung parliament. "
                    "Coverage raised the prospect that Labour could outperform its poll numbers."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "UK votes: Election day arrives with Conservatives ahead in polls",
                "article_date": "2019-12-11",
                "article_summary": (
                    "BBC News reported the polling evidence without translating it into an explicit seat or majority prediction, "
                    "consistent with the corporation's convention of not forecasting electoral outcomes. "
                    "Coverage set out the parties' final arguments and key battleground seats."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Boris Johnson on course for majority as Conservatives hold polling lead on election eve",
                "article_date": "2019-12-11",
                "article_summary": (
                    "The Telegraph was explicit in predicting a Conservative majority, citing the consistent double-digit polling lead "
                    "and internal party confidence about marginal seat performance. "
                    "Coverage framed a Johnson majority as the expected outcome."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Johnson headed for majority as voters prepare to go to polls",
                "article_date": "2019-12-11",
                "article_summary": (
                    "The Times reported the polling evidence as pointing clearly to a Conservative majority, "
                    "with analysis suggesting the seat arithmetic favoured Johnson even on conservative turnout assumptions. "
                    "Coverage framed the election as Johnson's to lose."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain votes with Johnson's Conservatives ahead in polls",
                "article_date": "2019-12-11",
                "article_summary": (
                    "Reuters reported the polling picture factually and noted analyst consensus that a Conservative majority was the most likely outcome, "
                    "contextualising the election within the Brexit impasse. "
                    "Coverage was measured but reflected the polling consensus."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Election 2019: Polls point to Conservative victory but seat predictions vary widely",
                "article_date": "2019-12-11",
                "article_summary": (
                    "Sky News reported the polling lead and seat projections pointing to a Conservative majority, "
                    "with political correspondents noting the scale of the lead made a hung parliament unlikely. "
                    "Coverage did not rule out surprises but framed Johnson's victory as probable."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 13 — Dominic Cummings Departure November 2020
    # -----------------------------------------------------------------------
    {
        "event_id": 13,
        "event_name": "Dominic Cummings Departure November 2020",
        "event_date": "2020-11-13",
        "initial_coverage_date": "2020-11-12",
        "resolution_time_hours": 24,
        "event_category": "Scandal",
        "outcome": "Dominic Cummings departed Downing Street on 13 November 2020, carrying a box of belongings, in what Downing Street confirmed was his final day as chief adviser to Boris Johnson.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Reports emerged on 12 November 2020 of an acute power struggle inside Downing Street "
            "between Dominic Cummings and director of communications Lee Cain on one side, "
            "and others including Boris Johnson's partner Carrie Symonds on the other. "
            "Lee Cain resigned as communications director on 12 November. "
            "Reports suggest Cummings's own position has become untenable following the internal conflict, "
            "but Downing Street has not confirmed whether he will leave or remain as chief adviser."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A fast-resolution Scandal event (24 hours) driven by an internal power struggle rather than public conduct. "
            "Tests whether outlets with better Downing Street sourcing (Guardian, Times) predicted departure more accurately "
            "than those relying on official channels. "
            "Cummings's subsequent public claims about the circumstances of his departure add retrospective context."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Dominic Cummings's position at No 10 under threat after Cain resignation",
                "article_date": "2020-11-12",
                "article_summary": (
                    "The Guardian reported the power struggle inside Downing Street and indicated that Cummings's position "
                    "had become untenable following Cain's departure. "
                    "Coverage suggested Cummings would depart imminently, citing sources close to the conflict."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Dominic Cummings future at No 10 uncertain after Lee Cain resignation",
                "article_date": "2020-11-12",
                "article_summary": (
                    "BBC News reported the power struggle and Cain's departure factually, noting that Cummings's own "
                    "position was being questioned but that Downing Street had not confirmed his departure. "
                    "Coverage was measured about forecasting his fate."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Cummings future at No 10 in doubt after communications chief Cain quits",
                "article_date": "2020-11-12",
                "article_summary": (
                    "The Telegraph, which had been broadly sympathetic to Cummings's agenda, reported the internal chaos "
                    "with uncertainty about whether he would depart. "
                    "Coverage noted Johnson had previously stood by Cummings through the Durham lockdown controversy."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Cummings expected to leave No 10 after Cain exit triggers Downing Street crisis",
                "article_date": "2020-11-12",
                "article_summary": (
                    "The Times reported that Cummings was expected to depart imminently, "
                    "citing sources indicating the internal conflict had reached a point of no return. "
                    "Coverage framed his departure as likely within days."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Johnson's top aide Cummings faces uncertain future after ally quits",
                "article_date": "2020-11-12",
                "article_summary": (
                    "Reuters reported the Cain resignation and the internal Downing Street conflict factually, "
                    "noting that Cummings's position had become uncertain. "
                    "No explicit forecast was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Dominic Cummings could be next to leave No 10 after Cain departure",
                "article_date": "2020-11-12",
                "article_summary": (
                    "Sky News reported that sources indicated Cummings was likely to follow Cain out of Downing Street, "
                    "with political correspondents citing the severity of the internal conflict. "
                    "Coverage suggested departure was probable but not certain."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 14 — Sue Gray Partygate Report May 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 14,
        "event_name": "Sue Gray Partygate Report May 2022",
        "event_date": "2022-05-25",
        "initial_coverage_date": "2022-05-23",
        "resolution_time_hours": 48,
        "event_category": "Scandal",
        "outcome": "Sue Gray published her full Partygate report on 25 May 2022, confirming widespread rule-breaking at Downing Street during Covid lockdowns; Boris Johnson survived the immediate political fallout and remained Prime Minister.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "Senior civil servant Sue Gray is expected to publish her full report into gatherings held at "
            "Downing Street and other government buildings during Covid lockdown restrictions imminently, "
            "following an interim report published in January 2022. "
            "The Metropolitan Police concluded its investigation in May 2022, issuing 126 fixed penalty notices "
            "including to Boris Johnson. "
            "Reports on 23 May indicate the full Gray report will be published within days and is expected "
            "to be highly critical of the culture in Downing Street. "
            "Whether its findings will be severe enough to force Johnson's resignation is contested."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Scandal event where the outcome was SURVIVED — Johnson did not resign immediately after the report. "
            "Tests whether outlets that predicted WILL_RESIGN (Guardian, Times) are coded FALSE, "
            "while those predicting WILL_SURVIVE (Telegraph) are coded TRUE. "
            "Useful for examining whether anti-government framing bias leads to over-prediction of resignation events."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Sue Gray full partygate report imminent and expected to be damning for Johnson",
                "article_date": "2022-05-23",
                "article_summary": (
                    "The Guardian framed the imminent Gray report as likely to be sufficiently damaging to finally end Johnson's premiership, "
                    "citing sources indicating the findings would include photographic evidence of gatherings. "
                    "Coverage suggested the report could be the moment Conservative MPs finally moved against him."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Sue Gray partygate report to be published this week, government confirms",
                "article_date": "2022-05-23",
                "article_summary": (
                    "BBC News reported the imminent publication of the Gray report without speculating on whether Johnson would resign following its findings. "
                    "Coverage set out what the report was expected to cover and how Conservative MPs had said they would respond."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Johnson set to survive Gray report as Tory MPs say findings already priced in",
                "article_date": "2022-05-23",
                "article_summary": (
                    "The Telegraph reported that senior Conservative MPs believed the Partygate scandal had already "
                    "caused its maximum political damage and that the Gray report was unlikely to produce enough new material to topple Johnson. "
                    "Coverage framed Johnson as likely to survive the publication."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Gray report set to be most damning verdict yet on Downing Street culture",
                "article_date": "2022-05-23",
                "article_summary": (
                    "The Times reported that the full Gray report would contain photographic evidence and more damaging detail than the interim version, "
                    "and suggested it could provide the trigger for a renewed confidence vote attempt against Johnson. "
                    "Coverage leaned toward WILL_RESIGN."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Johnson awaits publication of partygate inquiry report",
                "article_date": "2022-05-23",
                "article_summary": (
                    "Reuters reported the imminent Gray report publication in factual terms, "
                    "setting out the background of the Partygate investigation and Johnson's prior police fine. "
                    "No forecast was made about his political fate."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Sue Gray report due this week — will it be enough to end Johnson's premiership?",
                "article_date": "2022-05-23",
                "article_summary": (
                    "Sky News framed the publication as an open question about Johnson's survival, "
                    "reporting that the threshold for action among Conservative MPs remained unclear. "
                    "Coverage was balanced but noted the report alone was unlikely to be sufficient if MPs had already decided to wait."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 15 — Scotland IndyRef2 Supreme Court Ruling November 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 15,
        "event_name": "Scotland IndyRef2 Supreme Court Ruling 2022",
        "event_date": "2022-11-23",
        "initial_coverage_date": "2022-11-21",
        "resolution_time_hours": 48,
        "event_category": "Legal_Courts",
        "outcome": "The Supreme Court ruled unanimously on 23 November 2022 that the Scottish Parliament does not have the power to legislate for an independence referendum without the consent of the UK Parliament.",
        "outcome_binary": "BLOCKED",
        "event_description": (
            "The Scottish Government referred a question to the Supreme Court asking whether it had the power "
            "to legislate for a second independence referendum without a Section 30 order from Westminster. "
            "The court heard arguments on 11 and 12 October 2022. "
            "Reports on 21 November indicate the judgment is expected within days. "
            "The Scottish Government under Nicola Sturgeon argues the Holyrood parliament has the competence "
            "to legislate for a consultative referendum; the UK Government argues it does not. "
            "The legal question is finely balanced, according to constitutional experts."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Legal_Courts event where most outlets were genuinely uncertain about the legal outcome, "
            "providing a near-uniform UNCLEAR baseline. "
            "The Telegraph's unionist framing (WILL_LOSE for SNP) is the principal divergent signal. "
            "Useful for calibrating model behaviour when framing variance is low."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Supreme Court set to rule on Scottish independence referendum powers",
                "article_date": "2022-11-21",
                "article_summary": (
                    "The Guardian reported the imminent judgment with reference to both sides of the legal argument, "
                    "noting that constitutional experts were divided on whether Holyrood had the competence to legislate. "
                    "Coverage did not explicitly predict the outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Supreme Court to rule on Holyrood's power to hold independence referendum",
                "article_date": "2022-11-21",
                "article_summary": (
                    "BBC News reported the expected judgment in factual terms, setting out the legal question, "
                    "both governments' positions, and the implications of either verdict. "
                    "No prediction was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Supreme Court expected to block SNP bid for independence referendum",
                "article_date": "2022-11-21",
                "article_summary": (
                    "The Telegraph, with a broadly unionist editorial perspective, reported that legal analysts "
                    "expected the court to find against the Scottish Government, citing the constitutional limits of devolution. "
                    "Coverage leaned toward a BLOCKED outcome for the SNP's plans."
                ),
                "framing_prediction": "WILL_LOSE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Sturgeon faces pivotal moment as Supreme Court prepares independence ruling",
                "article_date": "2022-11-21",
                "article_summary": (
                    "The Times reported the imminent judgment as a pivotal moment for the Scottish independence movement, "
                    "noting that constitutional experts were cautious about predicting an outcome. "
                    "Coverage presented the legal question as genuinely contested."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Scotland's independence bid faces Supreme Court verdict",
                "article_date": "2022-11-21",
                "article_summary": (
                    "Reuters reported the expected ruling in factual terms, setting out the devolution framework "
                    "and the constitutional implications of either verdict for the SNP's independence strategy. "
                    "No legal prediction was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Supreme Court independence ruling due — what happens if Scotland wins or loses?",
                "article_date": "2022-11-21",
                "article_summary": (
                    "Sky News framed coverage around the implications of each possible verdict rather than predicting one, "
                    "setting out how Sturgeon had said she would respond to either outcome. "
                    "Coverage was balanced and did not forecast the ruling."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 16 — 2024 General Election Labour Win
    # -----------------------------------------------------------------------
    {
        "event_id": 16,
        "event_name": "2024 General Election Labour Win",
        "event_date": "2024-07-05",
        "initial_coverage_date": "2024-07-03",
        "resolution_time_hours": 48,
        "event_category": "Election_Leadership",
        "outcome": "Labour won a landslide majority of 412 seats at the 4 July 2024 general election; Keir Starmer became Prime Minister on 5 July 2024.",
        "outcome_binary": "WIN",
        "event_description": (
            "The United Kingdom is holding a general election on 4 July 2024, called by Rishi Sunak on 22 May 2024. "
            "Final polls published on 3 July consistently show Labour with a lead of 18 to 22 percentage points, "
            "which seat projection models translate into a Labour majority of between 150 and 200 seats. "
            "The Conservative Party is polling at historic lows. "
            "Whether the polls accurately capture final turnout patterns — and the precise scale of any Labour majority — "
            "remains to be confirmed by the result."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether near-universal WILL_WIN predictions for Labour (Guardian, Telegraph, Times, Reuters, Sky News) "
            "vs BBC's conventional UNCLEAR framing correctly forecast the WIN outcome. "
            "A low-disagreement event by design — polling was unusually clear — useful for calibrating "
            "what low VADER variance looks like in practice and verifying source accuracy on high-confidence events."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Labour on course for historic majority as final polls show record Conservative collapse",
                "article_date": "2024-07-03",
                "article_summary": (
                    "The Guardian reported the polling evidence as pointing decisively to a Labour landslide, "
                    "with coverage strongly framing a Labour win as the expected outcome. "
                    "Analysis focused on the likely scale of the majority rather than whether Labour would win."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Election 2024: Voters head to polls with Labour well ahead in surveys",
                "article_date": "2024-07-03",
                "article_summary": (
                    "BBC News reported the polling lead factually without translating it into an explicit prediction of a Labour majority. "
                    "Coverage set out both parties' final campaign messages and noted that historical polling errors meant certainty was impossible."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Tories face wipeout as final polls show Labour poised for landslide",
                "article_date": "2024-07-03",
                "article_summary": (
                    "Even the Telegraph — ordinarily a Conservative-supporting outlet — reported the polling picture as pointing to a Labour landslide, "
                    "with coverage focusing on the scale of the coming Conservative defeat rather than contesting the likely outcome. "
                    "Framing accepted Labour's win as expected."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Labour set for historic victory as Conservative poll collapse deepens",
                "article_date": "2024-07-03",
                "article_summary": (
                    "The Times reported polling evidence as pointing unambiguously to a Labour majority, "
                    "with seat projection analysis suggesting a majority of 150 to 200. "
                    "Coverage focused on what a Starmer government's first days would look like."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain votes in election that polls show will deliver Labour landslide",
                "article_date": "2024-07-03",
                "article_summary": (
                    "Reuters reported the polling picture factually, noting analyst consensus that Labour would win a substantial majority "
                    "and contextualising the election within the UK's cost-of-living and public services crises. "
                    "Coverage reflected the polling consensus without hedging."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Election 2024: Labour heading for landslide majority as voters go to polls",
                "article_date": "2024-07-03",
                "article_summary": (
                    "Sky News reported the polling lead and seat projections as pointing clearly to a Labour majority, "
                    "with political correspondents citing the consistency of the 18-22 point lead as giving high confidence. "
                    "Coverage explicitly framed a Labour win as the expected outcome."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 17 — Amber Rudd Resignation April 2018
    # -----------------------------------------------------------------------
    {
        "event_id": 17,
        "event_name": "Amber Rudd Resignation April 2018",
        "event_date": "2018-04-29",
        "initial_coverage_date": "2018-04-27",
        "resolution_time_hours": 48,
        "event_category": "Resignation",
        "outcome": "Amber Rudd resigned as Home Secretary on 29 April 2018 after it emerged she had misled Parliament by denying the existence of deportation targets for the Windrush generation.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Home Secretary Amber Rudd is facing intense pressure over the Windrush scandal, "
            "in which members of the Windrush generation — Commonwealth citizens who arrived in the UK between 1948 and 1971 — "
            "have been wrongly detained, denied legal rights, and in some cases deported. "
            "On 27 April 2018, leaked documents published by The Guardian revealed that the Home Office had set "
            "deportation targets for illegal immigrants, contradicting Rudd's statement to Parliament that no such targets existed. "
            "Rudd has issued a clarification but opposition parties are calling for her resignation and her position is under serious pressure."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets that identified the contradiction between Rudd's parliamentary statement and the leaked documents "
            "(Guardian, Times, Sky News — WILL_RESIGN) outperformed those hedging (BBC, Telegraph, Reuters — UNCLEAR). "
            "The Guardian's role in publishing the original leaked memo makes its source credibility particularly relevant here."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Amber Rudd's position as Home Secretary becomes untenable after leaked deportation targets",
                "article_date": "2018-04-27",
                "article_summary": (
                    "The Guardian, which had broken the Windrush story and published the leaked deportation targets memo, "
                    "framed Rudd's position as untenable given the direct contradiction between her parliamentary statement and the documentary evidence. "
                    "Coverage argued that knowingly misleading Parliament was a resigning matter under the ministerial code."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Amber Rudd faces calls to resign after leaked memo shows Home Office deportation targets",
                "article_date": "2018-04-27",
                "article_summary": (
                    "BBC News reported the leaked memo and the contradiction with Rudd's parliamentary statement factually, "
                    "noting opposition demands for her resignation. "
                    "Coverage set out her position — that she had not personally seen the memo — without forecasting whether she would survive."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Rudd under pressure over deportation targets memo but says she was unaware of document",
                "article_date": "2018-04-27",
                "article_summary": (
                    "The Telegraph reported Rudd's defence that she had not personally been aware of the targets memo, "
                    "giving reasonable space to her claim that the contradiction with her parliamentary statement was inadvertent. "
                    "Coverage did not rule out her survival if the personal knowledge defence held."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Amber Rudd misled Parliament on Windrush targets, leaked memo shows",
                "article_date": "2018-04-27",
                "article_summary": (
                    "The Times framed the leaked memo as evidence of a serious breach of parliamentary honesty, "
                    "reporting that the contradiction between Rudd's statement and the documentary record made her position "
                    "very difficult to defend regardless of whether she had personally seen the document. "
                    "Coverage suggested resignation was likely."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's interior minister faces calls to quit over Windrush deportation targets",
                "article_date": "2018-04-27",
                "article_summary": (
                    "Reuters reported the leaked memo and the political pressure on Rudd in factual terms, "
                    "setting out the Windrush scandal background and the opposition demands for her resignation. "
                    "No forecast was made about her political fate."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Amber Rudd's future as Home Secretary in doubt after deportation targets revelation",
                "article_date": "2018-04-27",
                "article_summary": (
                    "Sky News framed the leaked memo as placing Rudd's tenure in serious jeopardy, "
                    "with political correspondents reporting that Conservative MPs privately doubted she could survive the week. "
                    "Coverage noted that May's defence of Rudd was increasingly difficult to sustain."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 18 — Theresa May Resignation May 2019
    # -----------------------------------------------------------------------
    {
        "event_id": 18,
        "event_name": "Theresa May Resignation May 2019",
        "event_date": "2019-05-24",
        "initial_coverage_date": "2019-05-21",
        "resolution_time_hours": 72,
        "event_category": "Resignation",
        "outcome": "Theresa May announced her resignation as Prime Minister and Conservative Party leader on 24 May 2019, after failing to secure parliamentary approval for her Brexit Withdrawal Agreement on three separate occasions.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Theresa May's position as Prime Minister has become critically weakened following the third defeat "
            "of her Brexit Withdrawal Agreement on 29 March 2019 and the catastrophic Conservative performance "
            "in the 23 May 2019 European Parliament elections. "
            "Senior Cabinet ministers including Andrea Leadsom have begun to signal that May must set out a departure timetable. "
            "The 1922 Committee is reported to be considering changing its rules to allow an earlier confidence vote, "
            "having been barred from holding one for twelve months following the December 2018 contest. "
            "May met with Graham Brady on 21 May and is expected to announce a timetable for her departure imminently."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets expecting an imminent resignation announcement (Guardian, Times, Sky News — WILL_RESIGN) "
            "vs those allowing that May might delay further (BBC, Telegraph, Reuters — UNCLEAR) correctly predicted the "
            "24 May announcement. The European election results significantly hardened the framing by this date."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Theresa May's departure as PM imminent after Cabinet revolt and European election humiliation",
                "article_date": "2019-05-21",
                "article_summary": (
                    "The Guardian framed May's position as effectively over, reporting that Cabinet ministers had told her directly "
                    "she must announce a departure date following the catastrophic European election results. "
                    "Coverage cited multiple senior Conservative sources saying her continued presence was damaging the party's prospects."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Theresa May faces Cabinet pressure to set resignation timetable after European elections",
                "article_date": "2019-05-21",
                "article_summary": (
                    "BBC News reported the Cabinet pressure on May and the scale of the European election disaster factually, "
                    "noting that she had met with Brady but that Downing Street had not confirmed a departure timeline. "
                    "Coverage did not forecast the precise timing of any resignation announcement."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "May clings to office as Cabinet ministers demand she names departure date",
                "article_date": "2019-05-21",
                "article_summary": (
                    "The Telegraph reported the Cabinet pressure and the Brady meeting while noting that May was "
                    "reportedly determined to remain in post long enough to introduce her new Brexit deal in Parliament. "
                    "Coverage acknowledged the pressure was overwhelming but noted May's characteristic resilience."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Theresa May to announce resignation date this week as Cabinet support collapses",
                "article_date": "2019-05-21",
                "article_summary": (
                    "The Times reported that May had been told by senior Cabinet figures she must announce her departure date within days, "
                    "with sources indicating she had accepted the situation and was preparing her resignation statement. "
                    "Coverage framed the announcement as days away at most."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM May faces calls for resignation timetable after European election losses",
                "article_date": "2019-05-21",
                "article_summary": (
                    "Reuters reported the Cabinet pressure on May and the European election results factually, "
                    "noting her meeting with Brady and the scale of the internal Conservative party discontent. "
                    "No forecast was made about the timing of a departure announcement."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Theresa May's time as PM all but over as Cabinet turns against her",
                "article_date": "2019-05-21",
                "article_summary": (
                    "Sky News framed May's situation as effectively terminal, reporting that multiple Cabinet ministers had "
                    "told her directly she could not continue and that a resignation announcement was expected imminently. "
                    "Political editor Sophy Ridge reported that Downing Street was in preparations for a departure statement."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 19 — Nicola Sturgeon Resignation February 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 19,
        "event_name": "Nicola Sturgeon Resignation February 2023",
        "event_date": "2023-02-15",
        "initial_coverage_date": "2023-02-13",
        "resolution_time_hours": 48,
        "event_category": "Resignation",
        "outcome": "Nicola Sturgeon announced her resignation as First Minister of Scotland and SNP leader on 15 February 2023, citing the personal toll of the role after eight years in office.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Nicola Sturgeon called a press conference for 11am on 15 February 2023. "
            "The purpose of the announcement had not been confirmed in advance and speculation was widespread. "
            "Sturgeon had faced a difficult period including the collapse of the Deposit Return Scheme, "
            "ongoing controversy over the Gender Recognition Reform Bill following the UK Government's section 35 order, "
            "and questions about the direction of the independence campaign after the Supreme Court ruling. "
            "Reports on 13 February suggested the announcement could be significant but its nature was genuinely unknown."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An unusual Resignation event because the outcome was genuinely unexpected — most outlets were UNCLEAR "
            "in the two days before the announcement. Tests whether any outlet had specific intelligence "
            "about the nature of the announcement. High UNCLEAR rate across all sources is itself a valid "
            "data point for calibrating model uncertainty on low-signal events."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Nicola Sturgeon calls press conference amid speculation over major announcement",
                "article_date": "2023-02-13",
                "article_summary": (
                    "The Guardian reported that Sturgeon had called a significant press conference without specifying its subject, "
                    "noting the difficult political period she had faced. "
                    "Coverage raised the possibility of a leadership announcement but did not commit to predicting resignation, "
                    "noting Sturgeon had weathered previous challenges."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Nicola Sturgeon to make major statement — what could it be?",
                "article_date": "2023-02-13",
                "article_summary": (
                    "BBC Scotland reported the imminent Sturgeon press conference factually, setting out the range of possibilities "
                    "from a policy announcement to a leadership statement. "
                    "Coverage did not predict the content of the announcement and quoted Scottish political commentators expressing genuine uncertainty."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Nicola Sturgeon press conference fuels speculation — resignation possible, sources suggest",
                "article_date": "2023-02-13",
                "article_summary": (
                    "The Telegraph reported that sources close to the SNP had suggested the announcement could be a leadership statement, "
                    "citing the accumulation of political difficulties Sturgeon had faced. "
                    "Coverage was cautious but leaned toward the possibility of a resignation announcement."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Sturgeon resignation possible as SNP sources point to leadership announcement",
                "article_date": "2023-02-13",
                "article_summary": (
                    "The Times reported that SNP sources had indicated the press conference was likely to address Sturgeon's future, "
                    "citing the personal toll of the role and the political headwinds she faced. "
                    "Coverage raised the resignation possibility explicitly."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Scotland's Sturgeon calls press conference; purpose unconfirmed",
                "article_date": "2023-02-13",
                "article_summary": (
                    "Reuters reported the scheduled press conference factually, noting the range of possible subjects "
                    "and the political context of Sturgeon's recent difficulties. "
                    "No prediction was made about the nature of the announcement."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Sturgeon to make major announcement — resignation speculation grows",
                "article_date": "2023-02-13",
                "article_summary": (
                    "Sky News reported that speculation about a potential Sturgeon resignation was growing ahead of the press conference, "
                    "with political correspondents noting the unusual circumstances of the announcement. "
                    "Coverage presented resignation as a genuine possibility without predicting it definitively."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 20 — Cressida Dick Resignation February 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 20,
        "event_name": "Cressida Dick Resignation February 2022",
        "event_date": "2022-02-10",
        "initial_coverage_date": "2022-02-08",
        "resolution_time_hours": 48,
        "event_category": "Resignation",
        "outcome": "Metropolitan Police Commissioner Cressida Dick resigned on 10 February 2022 after Mayor of London Sadiq Khan stated he had no confidence in her leadership following a series of scandals including the murder of Sarah Everard by a serving officer.",
        "outcome_binary": "RESIGNED",
        "event_description": (
            "Metropolitan Police Commissioner Cressida Dick is facing calls for her resignation following a series of institutional scandals, "
            "including the murder of Sarah Everard by serving officer Wayne Couzens, "
            "the dismissal of officers for sharing racist and misogynistic messages, "
            "and controversies over the policing of the Sarah Everard vigil. "
            "On 8 February 2022, Mayor of London Sadiq Khan held a meeting with Dick and subsequently told reporters "
            "he did not believe she had a sufficient plan to tackle the Met's cultural problems. "
            "Whether Khan's public loss of confidence will be enough to force her departure is not yet confirmed."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets that interpreted Khan's statement as effectively forcing Dick out (Guardian, Times, Sky News) "
            "vs those allowing she might resist (BBC, Telegraph, Reuters) correctly predicted the RESIGNED outcome. "
            "Unusual in that the proximate trigger was a mayoral rather than a governmental loss of confidence."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Cressida Dick's position as Met chief untenable after Sadiq Khan withdraws confidence",
                "article_date": "2022-02-08",
                "article_summary": (
                    "The Guardian framed Khan's public loss of confidence as effectively making Dick's position untenable, "
                    "reporting that a Commissioner who had lost the confidence of the Mayor could not continue. "
                    "Coverage cited policing experts arguing the institutional damage required new leadership."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Cressida Dick faces calls to resign after Mayor Khan loses confidence in Met chief",
                "article_date": "2022-02-08",
                "article_summary": (
                    "BBC News reported Khan's statement and the calls for Dick's resignation factually, "
                    "noting the constitutional complexity of a Commissioner's removal and that Dick had not yet indicated "
                    "she intended to stand down. "
                    "Coverage did not forecast whether she would resign."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Cressida Dick vows to fight on as Mayor Khan demands reform of Metropolitan Police",
                "article_date": "2022-02-08",
                "article_summary": (
                    "The Telegraph reported that Dick had signalled her intention to remain in post despite Khan's statement, "
                    "noting that the Home Secretary rather than the Mayor had the formal power to remove a Commissioner. "
                    "Coverage raised the question of whether Dick could outlast the political pressure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Cressida Dick's resignation as Met Commissioner expected within days after Khan ultimatum",
                "article_date": "2022-02-08",
                "article_summary": (
                    "The Times reported that sources close to the Met expected Dick to stand down within days following Khan's statement, "
                    "noting that continuing without the Mayor's confidence was operationally untenable. "
                    "Coverage framed her departure as effectively a matter of when, not whether."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "London Mayor Khan loses confidence in Metropolitan Police Commissioner Dick",
                "article_date": "2022-02-08",
                "article_summary": (
                    "Reuters reported Khan's statement and its political significance factually, "
                    "contextualising the Met's recent scandals and the governance relationship between the Mayor and Commissioner. "
                    "No prediction was made about Dick's departure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Metropolitan Police Commissioner Cressida Dick's position under serious threat after Khan statement",
                "article_date": "2022-02-08",
                "article_summary": (
                    "Sky News reported that policing sources believed Dick would struggle to continue following Khan's public withdrawal of confidence, "
                    "with political correspondents noting the cumulative institutional damage to the Met. "
                    "Coverage suggested resignation was the likely outcome."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 21 — HS2 Northern Leg Cancellation October 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 21,
        "event_name": "HS2 Northern Leg Cancellation October 2023",
        "event_date": "2023-10-04",
        "initial_coverage_date": "2023-10-01",
        "resolution_time_hours": 72,
        "event_category": "Economic_Policy",
        "outcome": "Rishi Sunak announced at the Conservative Party conference on 4 October 2023 the cancellation of HS2's northern leg between Birmingham and Manchester, redirecting funds to alternative transport projects.",
        "outcome_binary": "CANCELLED",
        "event_description": (
            "Reports have emerged ahead of the Conservative Party conference in Manchester that Rishi Sunak "
            "is considering cancelling the Birmingham to Manchester leg of HS2. "
            "The project has faced repeated cost overruns, with the Office of Rail and Road estimating total costs "
            "could reach £71 billion in 2019 prices. "
            "Sunak has ordered a review of the remaining HS2 phases and is expected to make a major infrastructure announcement "
            "during his conference speech on 4 October. "
            "Whether he will cancel the northern leg entirely or announce a scaled-back version remains uncertain."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An Economic_Policy event where leaks to multiple outlets produced high pre-announcement certainty. "
            "Tests whether the outlets that received advance briefings (Times, Telegraph) and those that extrapolated from "
            "cost overrun reporting (Guardian, Sky News) outperformed those relying on official channels. "
            "The cancellation of a flagship infrastructure project provides a clear binary outcome for credibility assessment."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Rishi Sunak set to cancel HS2 northern leg at Conservative conference, sources say",
                "article_date": "2023-10-01",
                "article_summary": (
                    "The Guardian reported that sources close to the government had indicated Sunak would use his conference speech "
                    "to announce the cancellation of the Manchester leg, redirecting funds to regional road and rail projects. "
                    "Coverage framed the decision as a significant policy U-turn driven by cost overruns."
                ),
                "framing_prediction": "WILL_CANCEL",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "HS2 northern leg future uncertain as Sunak conference speech approaches",
                "article_date": "2023-10-01",
                "article_summary": (
                    "BBC News reported the speculation about HS2's future factually, noting the cost pressures and Sunak's infrastructure review "
                    "without confirming that cancellation had been decided. "
                    "Coverage presented both cancellation and a scaled-back version as possible outcomes."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Sunak to axe HS2 Manchester leg at conference in major infrastructure shift",
                "article_date": "2023-10-01",
                "article_summary": (
                    "The Telegraph reported that government sources had confirmed Sunak would announce the cancellation "
                    "of the Birmingham to Manchester leg and redirect funding to other transport improvements. "
                    "Coverage framed the decision as fiscally responsible given the project's spiralling costs."
                ),
                "framing_prediction": "WILL_CANCEL",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Sunak to cancel HS2 northern extension and announce alternative transport fund",
                "article_date": "2023-10-01",
                "article_summary": (
                    "The Times reported that the cancellation had been decided and that Sunak would announce an alternative "
                    "transport investment package called Network North in its place. "
                    "Coverage cited Treasury sources confirming the decision."
                ),
                "framing_prediction": "WILL_CANCEL",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Sunak expected to scale back HS2 rail project amid cost concerns",
                "article_date": "2023-10-01",
                "article_summary": (
                    "Reuters reported the HS2 cost pressures and the speculation about Sunak's conference announcement in factual terms, "
                    "noting that the project had become a political liability. "
                    "Coverage did not confirm cancellation, framing the outcome as uncertain."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "HS2 Manchester leg to be cancelled by Sunak at Conservative conference, Sky News understands",
                "article_date": "2023-10-01",
                "article_summary": (
                    "Sky News reported that its sources understood the cancellation of the Manchester leg had been confirmed "
                    "and would be announced during Sunak's conference speech. "
                    "Political correspondents framed the decision as the end of the original HS2 vision."
                ),
                "framing_prediction": "WILL_CANCEL",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 22 — Rwanda Plan Supreme Court Ruling November 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 22,
        "event_name": "Rwanda Plan Supreme Court Ruling November 2023",
        "event_date": "2023-11-15",
        "initial_coverage_date": "2023-11-13",
        "resolution_time_hours": 48,
        "event_category": "Legal_Courts",
        "outcome": "The UK Supreme Court ruled unanimously on 15 November 2023 that the government's Rwanda deportation policy was unlawful, finding that Rwanda could not be considered a safe third country for asylum seekers.",
        "outcome_binary": "BLOCKED",
        "event_description": (
            "The UK Supreme Court is due to deliver its judgment on the government's Rwanda asylum policy on 15 November 2023. "
            "The policy — under which asylum seekers who arrive in the UK through irregular means would be removed to Rwanda "
            "for processing — was ruled unlawful by the Court of Appeal in June 2023. "
            "The government appealed to the Supreme Court, arguing Rwanda was a safe third country. "
            "Constitutional and human rights lawyers are divided on whether the Supreme Court will uphold the "
            "Court of Appeal ruling or find in favour of the government."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Legal_Courts event where there was genuine legal uncertainty about the outcome. "
            "Tests whether outlets with human rights law expertise (Guardian) predicted the BLOCKED outcome "
            "against those applying a government-friendly reading of the safety evidence (Telegraph). "
            "The unanimous nature of the final ruling is relevant for assessing how well pre-ruling coverage "
            "captured the strength of the legal case against the policy."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Supreme Court Rwanda ruling expected to uphold ban on deportation flights, lawyers say",
                "article_date": "2023-11-13",
                "article_summary": (
                    "The Guardian reported that human rights lawyers and legal commentators widely expected the Supreme Court "
                    "to uphold the Court of Appeal's finding that Rwanda was not a safe third country. "
                    "Coverage cited expert opinion that the factual findings about Rwanda's asylum system were difficult to overturn on appeal."
                ),
                "framing_prediction": "WILL_BLOCK",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Supreme Court to rule on Rwanda deportation policy — what are the legal arguments?",
                "article_date": "2023-11-13",
                "article_summary": (
                    "BBC News reported the imminent ruling in factual terms, setting out both sides of the legal argument "
                    "and what each verdict would mean for the government's asylum policy. "
                    "Coverage noted legal experts were divided and did not forecast the outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Government hopes Supreme Court will overturn Rwanda ban and rescue asylum policy",
                "article_date": "2023-11-13",
                "article_summary": (
                    "The Telegraph, broadly supportive of the Rwanda policy, reported the government's confidence that the Supreme Court "
                    "would find in its favour on at least some grounds, citing legal sources suggesting the factual safety determination "
                    "was open to challenge. "
                    "Coverage presented the outcome as genuinely contested."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Rwanda policy faces likely defeat in Supreme Court, legal experts warn government",
                "article_date": "2023-11-13",
                "article_summary": (
                    "The Times reported that legal advisers within government had warned ministers the Rwanda policy was likely "
                    "to be ruled unlawful by the Supreme Court, citing the strength of the Court of Appeal's factual findings. "
                    "Coverage suggested the government was already preparing contingency legislation."
                ),
                "framing_prediction": "WILL_BLOCK",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Supreme Court prepares to rule on legality of Rwanda asylum scheme",
                "article_date": "2023-11-13",
                "article_summary": (
                    "Reuters reported the imminent Supreme Court ruling in factual terms, "
                    "setting out the policy background and the constitutional significance of the judgment. "
                    "No legal prediction was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Rwanda ruling due Wednesday — government braced for possible defeat",
                "article_date": "2023-11-13",
                "article_summary": (
                    "Sky News reported that government sources had indicated they were braced for an adverse ruling and "
                    "had contingency plans ready. "
                    "Political correspondents noted the legal consensus favoured the court upholding the earlier ban."
                ),
                "framing_prediction": "WILL_BLOCK",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 23 — Post Office Horizon Exoneration Legislation January 2024
    # -----------------------------------------------------------------------
    {
        "event_id": 23,
        "event_name": "Post Office Horizon Exoneration Legislation January 2024",
        "event_date": "2024-01-10",
        "initial_coverage_date": "2024-01-08",
        "resolution_time_hours": 48,
        "event_category": "Legal_Courts",
        "outcome": "Rishi Sunak announced on 10 January 2024 that the government would introduce emergency legislation to exonerate all postmasters wrongly convicted due to the faulty Horizon IT system.",
        "outcome_binary": "LEGISLATION_ANNOUNCED",
        "event_description": (
            "The ITV drama Mr Bates vs The Post Office, broadcast from 1 January 2024, triggered a major public and political "
            "response to the Post Office Horizon IT scandal, in which over 700 sub-postmasters were wrongly prosecuted "
            "for theft and false accounting due to errors in the Fujitsu Horizon computer system. "
            "Prime Minister Rishi Sunak is facing calls to legislate to bulk-exonerate all wrongly convicted postmasters "
            "rather than requiring each to go through individual appeals. "
            "As of 8 January, the government has not yet confirmed whether it will introduce emergency legislation, "
            "stating instead that the existing appeal process is the appropriate mechanism."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An unusual Legal_Courts event where public pressure from a television drama directly prompted a government policy reversal. "
            "Tests whether outlets that pushed for bulk exoneration legislation (Guardian, Times, Sky News) "
            "correctly predicted the government would announce it within 48 hours. "
            "The speed of the government's reversal makes this a useful case for source credibility on political pressure events."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Government must legislate to exonerate Horizon postmasters as public outrage grows",
                "article_date": "2024-01-08",
                "article_summary": (
                    "The Guardian argued strongly that the government had no choice but to introduce emergency legislation "
                    "following the ITV drama's impact on public opinion, reporting that senior Conservative MPs were pressing Sunak privately. "
                    "Coverage framed legislation as an imminent political necessity."
                ),
                "framing_prediction": "WILL_ACT",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Post Office scandal: Sunak faces pressure to legislate as ministers review options",
                "article_date": "2024-01-08",
                "article_summary": (
                    "BBC News reported the political pressure on Sunak to act and confirmed the government was reviewing its options, "
                    "without confirming that emergency legislation had been decided. "
                    "Coverage noted ministers had previously opposed bulk exoneration on legal grounds."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Sunak faces calls to exonerate Post Office victims as Horizon scandal grips public",
                "article_date": "2024-01-08",
                "article_summary": (
                    "The Telegraph reported the growing political pressure following the ITV drama and noted that Sunak's "
                    "previous reliance on the appeal process was coming under sustained attack from across the political spectrum. "
                    "Coverage suggested legislation was likely but had not been confirmed."
                ),
                "framing_prediction": "WILL_ACT",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Sunak to announce emergency Post Office legislation after TV drama sparks public fury",
                "article_date": "2024-01-08",
                "article_summary": (
                    "The Times reported that Sunak had decided to introduce emergency legislation and would announce it imminently, "
                    "citing sources indicating the government had reversed its earlier position following the scale of public reaction. "
                    "Coverage framed the announcement as days away."
                ),
                "framing_prediction": "WILL_ACT",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Sunak faces calls to clear Post Office Horizon wrongful conviction victims",
                "article_date": "2024-01-08",
                "article_summary": (
                    "Reuters reported the Post Office Horizon scandal and the political pressure on Sunak factually, "
                    "contextualising the scale of the wrongful prosecutions and the ITV drama's public impact. "
                    "No forecast was made about whether legislation would be announced."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Post Office victims to be exonerated by law, government expected to announce",
                "article_date": "2024-01-08",
                "article_summary": (
                    "Sky News reported that government sources indicated an emergency legislation announcement was being prepared, "
                    "with political correspondents noting Sunak could not sustain the previous position given the level of public anger. "
                    "Coverage indicated an announcement was imminent."
                ),
                "framing_prediction": "WILL_ACT",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 24 — Boris Johnson Privileges Committee Censure June 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 24,
        "event_name": "Boris Johnson Privileges Committee Censure June 2023",
        "event_date": "2023-06-15",
        "initial_coverage_date": "2023-06-12",
        "resolution_time_hours": 72,
        "event_category": "Scandal",
        "outcome": "The House of Commons Privileges Committee published its report on 15 June 2023, finding that Boris Johnson had deliberately misled Parliament over Partygate and recommending a 90-day suspension — a sanction that would have triggered a recall petition. Johnson had resigned his parliamentary seat on 9 June before the report was published.",
        "outcome_binary": "CENSURED",
        "event_description": (
            "The House of Commons Privileges Committee is expected to publish its report into whether Boris Johnson "
            "deliberately misled Parliament over Partygate gatherings at Downing Street. "
            "Johnson resigned his parliamentary seat on 9 June 2023, pre-empting the report's publication and "
            "denouncing the committee's process as a witch hunt. "
            "The committee's findings — including the severity of any recommended sanction — have not yet been published "
            "but leaks indicate the conclusions will be highly critical. "
            "Whether the report will find deliberate rather than inadvertent misleading, and what sanction it recommends, is not yet confirmed."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A Scandal event testing whether outlets with committee sources (Times, Guardian) correctly predicted "
            "the severity of the censure versus those allowing for a lesser finding (Telegraph, BBC). "
            "Johnson's pre-emptive resignation complicates the credibility assessment since the 90-day recommendation "
            "became largely symbolic — source credibility is assessed on whether the CENSURED outcome was predicted."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Boris Johnson faces damning privileges report finding of deliberate misleading",
                "article_date": "2023-06-12",
                "article_summary": (
                    "The Guardian reported that the Privileges Committee report was expected to find Johnson had deliberately "
                    "misled Parliament and to recommend a suspension long enough to trigger a recall petition. "
                    "Coverage cited sources familiar with the committee's conclusions, framing the outcome as a formal censure."
                ),
                "framing_prediction": "WILL_CENSURE",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Boris Johnson privileges report due this week after former PM's shock resignation",
                "article_date": "2023-06-12",
                "article_summary": (
                    "BBC News reported the imminent committee report in factual terms, noting Johnson's pre-emptive resignation "
                    "and his claim the process was politically motivated. "
                    "Coverage set out what the report could find without predicting the severity of the conclusions."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Johnson allies question legitimacy of privileges report as publication approaches",
                "article_date": "2023-06-12",
                "article_summary": (
                    "The Telegraph gave significant space to Johnson's allies who questioned the committee's impartiality "
                    "and argued the process had been politically motivated from the start. "
                    "Coverage noted the expected critical findings while allowing for the possibility that the severity "
                    "might be contested."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Privileges Committee to find Johnson deliberately misled Parliament, sources say",
                "article_date": "2023-06-12",
                "article_summary": (
                    "The Times reported that the committee had concluded Johnson deliberately — not inadvertently — misled "
                    "Parliament and would recommend a 90-day suspension. "
                    "Coverage cited committee sources and noted the finding would be the most severe parliamentary censure "
                    "in modern times."
                ),
                "framing_prediction": "WILL_CENSURE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Parliament panel to publish Johnson Partygate report after ex-PM's resignation",
                "article_date": "2023-06-12",
                "article_summary": (
                    "Reuters reported the imminent report publication and Johnson's pre-emptive resignation factually, "
                    "contextualising the Partygate investigation and the constitutional significance of a parliamentary censure. "
                    "No prediction was made about the findings."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Johnson privileges report to deliver severe verdict on former PM, Sky News understands",
                "article_date": "2023-06-12",
                "article_summary": (
                    "Sky News reported that its sources understood the committee report would deliver a severe censure, "
                    "finding deliberate misleading and recommending a suspension that would have triggered a recall petition. "
                    "Coverage noted the verdict would be the strongest possible short of expulsion."
                ),
                "framing_prediction": "WILL_CENSURE",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 25 — Conservative Leadership 2022: Liz Truss Wins
    # -----------------------------------------------------------------------
    {
        "event_id": 25,
        "event_name": "Conservative Leadership 2022 Liz Truss Wins",
        "event_date": "2022-09-05",
        "initial_coverage_date": "2022-09-01",
        "resolution_time_hours": 96,
        "event_category": "Election_Leadership",
        "outcome": "Liz Truss was announced as Conservative Party leader on 5 September 2022, defeating Rishi Sunak by 57.4% to 42.6% of the party membership vote.",
        "outcome_binary": "TRUSS_WINS",
        "event_description": (
            "The Conservative Party membership is voting between Foreign Secretary Liz Truss and former Chancellor "
            "Rishi Sunak to succeed Boris Johnson as party leader and Prime Minister. "
            "Polls of Conservative members have consistently shown Truss ahead by margins of 20 to 30 percentage points. "
            "The result will be announced on 5 September 2022. "
            "Truss has campaigned on immediate tax cuts and a rejection of the Treasury's economic orthodoxy, "
            "while Sunak has warned against unfunded tax reductions. "
            "The scale of Truss's polling lead makes her the clear favourite, though the precise margin of victory is uncertain."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A low-uncertainty Election_Leadership event where membership polls were unusually consistent. "
            "Tests whether outlets that translated polling certainty into a definitive TRUSS_WINS framing "
            "(Telegraph, Times, Guardian) outperformed those maintaining conventional UNCLEAR hedging (BBC, Reuters). "
            "The Telegraph's strong backing of Truss's economic programme makes its framing accuracy particularly relevant."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Liz Truss on course for comfortable Conservative leadership win over Sunak",
                "article_date": "2022-09-01",
                "article_summary": (
                    "The Guardian reported the polling evidence as pointing clearly to a Truss victory, "
                    "noting the consistency of the member polls and analysing what her economic programme would mean in practice. "
                    "Coverage framed a Truss win as the expected outcome while warning of the risks of her tax-cutting agenda."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Conservative leadership result due Monday with Truss ahead in polls",
                "article_date": "2022-09-01",
                "article_summary": (
                    "BBC News reported the polling lead and set out both candidates' positions without translating the evidence "
                    "into an explicit prediction. "
                    "Coverage noted membership polls could differ from final results and set out both leadership visions."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Liz Truss set for decisive Conservative leadership victory as members back her economic vision",
                "article_date": "2022-09-01",
                "article_summary": (
                    "The Telegraph, which had strongly backed Truss throughout the contest, reported the polling lead "
                    "as pointing to a decisive victory and framed her economic programme as a mandate for the supply-side reforms "
                    "the party needed. "
                    "Coverage was explicit in predicting a Truss win."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Truss expected to win Conservative leadership by comfortable margin on Monday",
                "article_date": "2022-09-01",
                "article_summary": (
                    "The Times reported the consistent polling advantage enjoyed by Truss and noted that Sunak's campaign "
                    "had failed to close the gap with the membership. "
                    "Coverage framed a Truss victory as the expected result."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's next PM to be announced Monday with Truss leading polls",
                "article_date": "2022-09-01",
                "article_summary": (
                    "Reuters reported the polling evidence and the forthcoming announcement factually, "
                    "noting Truss's consistent lead in member surveys. "
                    "Coverage reflected the polling consensus without making an explicit prediction."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Liz Truss poised to become next Conservative leader and Prime Minister",
                "article_date": "2022-09-01",
                "article_summary": (
                    "Sky News reported that Truss was poised to win the leadership contest based on polling evidence, "
                    "with political correspondents noting the scale and consistency of her lead made the result highly likely. "
                    "Coverage framed her victory as the expected outcome."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 26 — 2017 General Election Hung Parliament
    # -----------------------------------------------------------------------
    {
        "event_id": 26,
        "event_name": "2017 General Election Hung Parliament",
        "event_date": "2017-06-08",
        "initial_coverage_date": "2017-06-07",
        "resolution_time_hours": 24,
        "event_category": "Election_Leadership",
        "outcome": "The 2017 general election produced a hung Parliament; the Conservative Party under Theresa May won 317 seats — 13 fewer than in 2015 — and subsequently formed a confidence and supply agreement with the Democratic Unionist Party.",
        "outcome_binary": "HUNG_PARLIAMENT",
        "event_description": (
            "The United Kingdom is holding a snap general election on 8 June 2017, called by Theresa May to strengthen "
            "her mandate for Brexit negotiations. "
            "Final polls published on 7 June show a wide range of results: some showing a Conservative lead of 12 points, "
            "others as narrow as 1 point, reflecting an unusually volatile campaign in which Labour under Jeremy Corbyn "
            "significantly closed the gap from a 20-point Conservative lead at the start. "
            "Most seat projection models still forecast a Conservative majority, though with considerable uncertainty "
            "about the size."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A rare Election_Leadership event where the polling consensus was wrong. "
            "Tests whether any outlet correctly predicted the hung Parliament outcome against the dominant forecast of a "
            "Conservative majority. The Guardian's pro-Labour framing and the Telegraph's Conservative framing "
            "provide the key divergence. Useful for testing model behaviour when the outcome defied most source predictions."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Election too close to call as final polls show Labour closing the gap on Tories",
                "article_date": "2017-06-07",
                "article_summary": (
                    "The Guardian highlighted polls showing the gap narrowing dramatically, arguing that Labour's campaign "
                    "surge and youth turnout uncertainty made the outcome genuinely unpredictable. "
                    "Coverage raised the possibility of a hung Parliament more explicitly than most outlets."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "UK election: Polls diverge on eve of vote with Conservatives ahead on average",
                "article_date": "2017-06-07",
                "article_summary": (
                    "BBC News reported the divergence in final polls factually, noting that while the Conservatives led on average, "
                    "the range of outcomes in polling models was wide enough to include a hung Parliament. "
                    "Coverage did not forecast a specific outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Theresa May on course for increased majority as Conservative campaign holds lead",
                "article_date": "2017-06-07",
                "article_summary": (
                    "The Telegraph reported the average polling lead as pointing to a Conservative majority, "
                    "with coverage framing May's anticipated win as the expected outcome and focusing on the scale of the anticipated majority. "
                    "The possibility of a hung Parliament was not given significant weight."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "May expected to win majority but Labour surge narrows the gap on election eve",
                "article_date": "2017-06-07",
                "article_summary": (
                    "The Times reported the polling picture as still pointing to a Conservative majority but acknowledged "
                    "that Labour's campaign momentum had introduced real uncertainty. "
                    "Coverage was more cautious than early campaign forecasts but still leaned toward a May victory."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain votes in election with Conservatives ahead but outcome uncertain",
                "article_date": "2017-06-07",
                "article_summary": (
                    "Reuters reported the election day polling picture factually, noting the average Conservative lead "
                    "while acknowledging the volatility of the final surveys. "
                    "Coverage reflected the polling consensus without explicitly predicting a majority."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Election 2017: Polls point to Conservative win but Labour surge creates uncertainty",
                "article_date": "2017-06-07",
                "article_summary": (
                    "Sky News reported the polling range and noted that Labour's late momentum had made the outcome "
                    "less certain than at the start of the campaign. "
                    "Political correspondents presented a Conservative majority as the most likely outcome while not dismissing a hung Parliament."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 27 — Keir Starmer wins 2020 Labour Leadership
    # -----------------------------------------------------------------------
    {
        "event_id": 27,
        "event_name": "Keir Starmer Wins 2020 Labour Leadership",
        "event_date": "2020-04-04",
        "initial_coverage_date": "2020-04-02",
        "resolution_time_hours": 48,
        "event_category": "Election_Leadership",
        "outcome": "Keir Starmer won the Labour leadership contest on 4 April 2020 with 56.2% of first preference votes, defeating Rebecca Long-Bailey and Lisa Nandy to succeed Jeremy Corbyn.",
        "outcome_binary": "STARMER_WINS",
        "event_description": (
            "The Labour Party is concluding its leadership contest to succeed Jeremy Corbyn following the party's "
            "catastrophic 2019 general election defeat. "
            "The three candidates are Keir Starmer, Rebecca Long-Bailey, and Lisa Nandy. "
            "Internal party polling and constituency Labour party nominations have consistently pointed to Starmer "
            "as the clear frontrunner, with Long-Bailey — backed by the Corbynite left — in second place. "
            "The result will be announced on 4 April 2020. "
            "The scale of Starmer's lead in internal surveys makes him the overwhelming favourite."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A low-uncertainty Election_Leadership event where internal party polling was unusually clear. "
            "Tests whether outlets that translated the polling evidence into a definitive STARMER_WINS prediction "
            "(Guardian, Times, Sky News) outperformed those maintaining UNCLEAR hedging (BBC, Reuters). "
            "The Guardian's longstanding alignment with Labour internal dynamics makes its framing accuracy relevant."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Keir Starmer set for commanding Labour leadership victory on Saturday",
                "article_date": "2020-04-02",
                "article_summary": (
                    "The Guardian reported the internal party polling and CLP nominations as pointing clearly to a first-ballot "
                    "Starmer victory, noting that Long-Bailey had failed to close the gap despite the backing of the trade union left. "
                    "Coverage framed a Starmer win on the first count as the expected outcome."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Labour leadership result due Saturday with Starmer the favourite",
                "article_date": "2020-04-02",
                "article_summary": (
                    "BBC News reported the polling evidence and the forthcoming result without translating it into "
                    "an explicit first-ballot prediction. "
                    "Coverage set out the three candidates' positions and what different outcomes would mean for the party's direction."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Starmer favourite to win Labour leadership as contest concludes amid coronavirus crisis",
                "article_date": "2020-04-02",
                "article_summary": (
                    "The Telegraph reported the polling evidence pointing to a Starmer victory and analysed what his leadership "
                    "would mean for Labour's political positioning. "
                    "Coverage was broadly accurate in framing Starmer as the likely winner."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Keir Starmer to win Labour leadership with majority on first ballot, internal polls show",
                "article_date": "2020-04-02",
                "article_summary": (
                    "The Times reported that internal Labour polling and aggregated CLP nominations pointed to Starmer "
                    "winning a clear majority on the first count. "
                    "Coverage cited party sources indicating Long-Bailey's vote had not grown sufficiently to force a second preference count."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Labour Party to announce new leader Saturday with Starmer ahead in surveys",
                "article_date": "2020-04-02",
                "article_summary": (
                    "Reuters reported the contest and the forthcoming result in factual terms, noting Starmer's polling lead "
                    "and contextualising the leadership contest within Labour's post-2019 election reset. "
                    "No explicit prediction was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Keir Starmer expected to win Labour leadership race on Saturday",
                "article_date": "2020-04-02",
                "article_summary": (
                    "Sky News reported that Starmer was widely expected to win the contest on the first ballot, "
                    "citing polling evidence and the scale of his nomination support. "
                    "Coverage framed a Starmer victory as the anticipated outcome."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 28 — Kwasi Kwarteng Sacking October 2022
    # -----------------------------------------------------------------------
    {
        "event_id": 28,
        "event_name": "Kwasi Kwarteng Sacking October 2022",
        "event_date": "2022-10-14",
        "initial_coverage_date": "2022-10-12",
        "resolution_time_hours": 48,
        "event_category": "Scandal",
        "outcome": "Kwasi Kwarteng was sacked as Chancellor of the Exchequer by Liz Truss on 14 October 2022, becoming the second-shortest-serving Chancellor in UK history after 38 days in post.",
        "outcome_binary": "SACKED",
        "event_description": (
            "Chancellor Kwasi Kwarteng is facing intense pressure following the catastrophic market reaction to his "
            "23 September mini-budget, which triggered a sharp fall in the pound, a surge in gilt yields, and an "
            "emergency intervention by the Bank of England. "
            "On 3 October, Kwarteng reversed the abolition of the 45p top rate of income tax. "
            "The IMF issued an extraordinary public criticism of the government's economic plans on 11 October. "
            "Reports on 12 October suggest Truss is considering replacing Kwarteng as Chancellor ahead of a "
            "medium-term fiscal plan scheduled for 31 October, though Downing Street has not confirmed this."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "Tests whether outlets that identified the sacking as imminent (Guardian, Times, Sky News) "
            "vs those allowing that Kwarteng might survive until the October 31 fiscal plan (BBC, Telegraph, Reuters) "
            "correctly predicted the SACKED outcome. "
            "Distinct from Event 8 which covers the 45p U-turn: this event concerns the Chancellor's removal eleven days later."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Kwasi Kwarteng faces sacking as Truss considers replacing Chancellor before fiscal plan",
                "article_date": "2022-10-12",
                "article_summary": (
                    "The Guardian reported that government sources indicated Truss was actively considering replacing Kwarteng "
                    "before the October 31 fiscal statement, citing the IMF criticism and the continuing market instability. "
                    "Coverage framed a sacking as likely within days."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Kwasi Kwarteng under pressure as IMF criticises UK economic plans",
                "article_date": "2022-10-12",
                "article_summary": (
                    "BBC News reported the IMF criticism and the market pressure on the government's economic programme factually, "
                    "noting that Kwarteng's position was under scrutiny but that Downing Street had confirmed he remained in post. "
                    "Coverage did not forecast his departure."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Kwarteng vows to press ahead with economic plan despite IMF criticism and market pressure",
                "article_date": "2022-10-12",
                "article_summary": (
                    "The Telegraph, which had backed Kwarteng's supply-side economic agenda, reported his stated intention "
                    "to remain in post and deliver the October 31 fiscal plan. "
                    "Coverage acknowledged the pressure but presented survival as possible if markets stabilised."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Truss to sack Kwarteng and replace him as Chancellor, sources tell The Times",
                "article_date": "2022-10-12",
                "article_summary": (
                    "The Times reported that sources close to Truss had confirmed Kwarteng would be replaced as Chancellor "
                    "imminently, citing the need to reassure markets ahead of the fiscal statement. "
                    "Coverage indicated the sacking had been decided."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Chancellor Kwarteng faces calls to go as markets remain under pressure",
                "article_date": "2022-10-12",
                "article_summary": (
                    "Reuters reported the market pressure on Kwarteng and the IMF criticism factually, "
                    "noting that his position was under scrutiny without confirming a sacking was imminent. "
                    "No explicit forecast was made."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Kwasi Kwarteng could be replaced as Chancellor within days, Sky News understands",
                "article_date": "2022-10-12",
                "article_summary": (
                    "Sky News reported that sources indicated Truss was preparing to replace Kwarteng ahead of the fiscal plan, "
                    "with political correspondents noting that the IMF criticism had made his position untenable. "
                    "Coverage indicated a sacking was likely."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 29 — Theresa May Brexit Deal First Parliamentary Defeat January 2019
    # -----------------------------------------------------------------------
    {
        "event_id": 29,
        "event_name": "Theresa May Brexit Deal First Defeat January 2019",
        "event_date": "2019-01-15",
        "initial_coverage_date": "2019-01-13",
        "resolution_time_hours": 48,
        "event_category": "Economic_Policy",
        "outcome": "MPs rejected Theresa May's Brexit Withdrawal Agreement on 15 January 2019 by 432 votes to 202 — a majority of 230 — the largest government defeat in the modern Parliamentary era.",
        "outcome_binary": "DEFEATED",
        "event_description": (
            "Theresa May's Brexit Withdrawal Agreement is due to be voted on by the House of Commons on 15 January 2019, "
            "having been delayed from December 2018 when May pulled the vote to avoid defeat. "
            "Whipping counts by opposition parties and rebel Conservative MPs indicate the government faces a very heavy defeat. "
            "Estimates of the likely majority against range from 100 to over 200. "
            "May has made last-minute attempts to secure assurances from the EU on the Northern Ireland backstop "
            "but EU leaders have not offered legally binding changes. "
            "The scale of the likely defeat — and what it means for the Brexit process — is uncertain."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An Economic_Policy event where the outcome (defeat) was widely expected but the scale was uncertain. "
            "Tests whether outlets predicting a historic defeat (Guardian, Times) correctly characterised the scale "
            "versus those who left the margin open. "
            "The record 230-majority defeat exceeded most estimates and is useful for calibrating how sources "
            "handle the difference between direction and magnitude of a policy outcome."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Theresa May set for record Brexit defeat as Conservative rebels hold firm",
                "article_date": "2019-01-13",
                "article_summary": (
                    "The Guardian reported that whipping counts pointed to a very heavy government defeat, "
                    "with Conservative rebels and opposition parties together likely to produce a majority of over 100. "
                    "Coverage framed the vote as a near-certain defeat and focused on the political consequences for May."
                ),
                "framing_prediction": "WILL_DEFEAT",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Brexit vote: May faces heavy defeat with rebels showing no sign of backing deal",
                "article_date": "2019-01-13",
                "article_summary": (
                    "BBC News reported the government's expected defeat factually, noting that rebel counts indicated "
                    "the government would lose by a substantial margin. "
                    "Coverage set out the range of possible majorities without predicting the precise scale."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "May faces certain Brexit defeat but vows to press on as rebels hold firm",
                "article_date": "2019-01-13",
                "article_summary": (
                    "The Telegraph reported the expected defeat and May's stated determination to continue pursuing Brexit "
                    "regardless of the margin. "
                    "Coverage acknowledged the scale of the likely defeat but focused on May's plan to continue negotiating with the EU."
                ),
                "framing_prediction": "WILL_DEFEAT",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Brexit deal heading for record parliamentary defeat as rebel majority grows",
                "article_date": "2019-01-13",
                "article_summary": (
                    "The Times reported that whipping counts now pointed to a defeat of over 200, which would be the "
                    "largest government Commons defeat in modern parliamentary history. "
                    "Coverage framed the vote as a near-certain defeat and analysed the constitutional consequences."
                ),
                "framing_prediction": "WILL_DEFEAT",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM May faces near-certain Brexit vote defeat on Tuesday",
                "article_date": "2019-01-13",
                "article_summary": (
                    "Reuters reported the expected parliamentary defeat factually, "
                    "noting that rebel counts made a government loss highly likely and contextualising the vote "
                    "within the broader Brexit negotiating process. "
                    "Coverage reflected the political consensus without specifying the likely margin."
                ),
                "framing_prediction": "WILL_DEFEAT",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "May's Brexit deal heading for crushing Commons defeat with no last-minute EU lifeline",
                "article_date": "2019-01-13",
                "article_summary": (
                    "Sky News reported that EU leaders had offered no new legally binding assurances and that "
                    "Conservative rebels were holding firm, making a heavy defeat certain. "
                    "Political correspondents noted the defeat could be the largest in modern parliamentary history."
                ),
                "framing_prediction": "WILL_DEFEAT",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 30 — Rishi Sunak Net Zero Policy Retreat September 2023
    # -----------------------------------------------------------------------
    {
        "event_id": 30,
        "event_name": "Rishi Sunak Net Zero Policy Retreat September 2023",
        "event_date": "2023-09-20",
        "initial_coverage_date": "2023-09-18",
        "resolution_time_hours": 48,
        "event_category": "Economic_Policy",
        "outcome": "Rishi Sunak announced on 20 September 2023 a rollback of several net zero commitments, including delaying the ban on new petrol and diesel cars from 2030 to 2035 and pushing back mandatory heat pump installation targets.",
        "outcome_binary": "WEAKENED",
        "event_description": (
            "Reports have emerged ahead of an expected Downing Street statement that Rishi Sunak is preparing "
            "to water down several of the UK's net zero policy commitments. "
            "Briefings on 18 September indicate the government may push back the 2030 ban on new petrol and diesel cars "
            "to 2035 and delay mandatory heat pump installation targets. "
            "The policy has not yet been formally announced and the government has not confirmed the reports, "
            "though Sunak is expected to make a statement to the press early in the week of 18 September."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "An Economic_Policy event where pre-announcement leaks produced high certainty across most outlets. "
            "Tests whether the outlets receiving government briefings (Times, Telegraph) predicted the WEAKENED outcome "
            "most clearly. "
            "Provides a useful contrast with Event 21 (HS2 cancellation) as a second Sunak economic U-turn event "
            "tested in the same political period."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Sunak to water down net zero targets in major policy retreat, sources say",
                "article_date": "2023-09-18",
                "article_summary": (
                    "The Guardian reported that sources had confirmed Sunak intended to push back the 2030 car ban "
                    "and weaken other net zero commitments in an announcement expected within days. "
                    "Coverage framed the move as a significant retreat from UK climate commitments and predicted the "
                    "announcement would trigger cross-party criticism."
                ),
                "framing_prediction": "WILL_WEAKEN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Sunak considering changes to net zero car and heat pump targets",
                "article_date": "2023-09-18",
                "article_summary": (
                    "BBC News reported that the government was considering changes to the 2030 car ban and heat pump targets "
                    "without confirming that a formal announcement had been decided. "
                    "Coverage presented the policy review as ongoing and noted Sunak had not yet committed to specific changes."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Sunak to delay 2030 petrol car ban to 2035 in net zero reset announcement",
                "article_date": "2023-09-18",
                "article_summary": (
                    "The Telegraph reported that the delay of the 2030 car ban to 2035 had been confirmed by government "
                    "sources, framing the decision as a pragmatic recalibration that would ease the cost burden on motorists. "
                    "Coverage was broadly supportive of the policy change."
                ),
                "framing_prediction": "WILL_WEAKEN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Sunak set to push back green targets in net zero announcement this week",
                "article_date": "2023-09-18",
                "article_summary": (
                    "The Times reported that the announcement had been prepared and would be made within 48 hours, "
                    "citing Downing Street sources who confirmed the 2030 car ban would be delayed to 2035 and "
                    "heat pump targets relaxed. "
                    "Coverage framed the policy shift as a deliberate electoral calculation."
                ),
                "framing_prediction": "WILL_WEAKEN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Sunak to review net zero commitments including electric vehicle targets",
                "article_date": "2023-09-18",
                "article_summary": (
                    "Reuters reported the expected policy review and likely changes factually, "
                    "contextualising the UK's net zero commitments and the economic pressures Sunak cited. "
                    "Coverage noted the change was expected but did not confirm it had been formally decided."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Sunak to announce net zero policy changes including 2030 car ban delay, Sky News understands",
                "article_date": "2023-09-18",
                "article_summary": (
                    "Sky News reported that its sources had confirmed the announcement of the 2030 car ban delay to 2035 "
                    "and changes to heat pump targets, with the statement expected on 20 September. "
                    "Coverage noted the move would be criticised by climate groups and opposition parties."
                ),
                "framing_prediction": "WILL_WEAKEN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 31 — Theresa May Survives Chequers Cabinet Resignations July 2018
    # -----------------------------------------------------------------------
    {
        "event_id": 31,
        "event_name": "Theresa May Survives Chequers Cabinet Resignations July 2018",
        "event_date": "2018-07-11",
        "initial_coverage_date": "2018-07-09",
        "resolution_time_hours": 48,
        "event_category": "Resignation",
        "outcome": "Theresa May reshuffled her cabinet and continued as Prime Minister, appointing Dominic Raab as Brexit Secretary and pressing ahead with the Chequers plan despite losing Davis and Johnson.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "David Davis and Boris Johnson have both resigned from Theresa May's cabinet within 24 hours, with Johnson quitting as Foreign Secretary this morning citing the Chequers Brexit deal as leaving Britain a 'colony' of the EU. "
            "The twin resignations have left May severely weakened, having lost her two most senior Brexiteer ministers simultaneously. "
            "She is due to face the Commons and must convince Conservative MPs that she can hold the government together and deliver Brexit. "
            "Westminster is gripped by speculation over whether further resignations will follow and whether May's position is now untenable."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "The Guardian, Times, and Sky News all predicted the scale of cabinet losses would force May to resign, making this event valuable for testing whether outlets systematically over-predicted Conservative PM departures after senior minister walkouts."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "May's Position Untenable After Johnson and Davis Quit, Say Tory MPs",
                "article_date": "2018-07-09",
                "article_summary": (
                    "The Guardian reports that senior Conservative MPs are telling the paper that Theresa May's position as Prime Minister is no longer tenable following the resignations of Boris Johnson and David Davis. "
                    "Multiple anonymous backbenchers say they cannot see how she survives the week, and that the 1922 Committee is already discussing a confidence vote. "
                    "The Guardian's political editor argues that May lacks the authority to continue and the party will move quickly to replace her."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Johnson Resigns: What Happens Next for Theresa May?",
                "article_date": "2018-07-09",
                "article_summary": (
                    "The BBC examines the political fallout from Boris Johnson's resignation as Foreign Secretary, following David Davis's departure the previous evening. "
                    "Political correspondents note that May faces severe pressure from multiple directions but that the immediate trigger for a confidence vote — 48 letters to the 1922 Committee — has not yet been reached. "
                    "The BBC presents both possible outcomes, noting that past Prime Ministers have survived similar crises."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "May Vows to Fight On as She Reshuffles Cabinet After Brexiteer Walkout",
                "article_date": "2018-07-09",
                "article_summary": (
                    "The Telegraph reports that Theresa May is determined to continue as Prime Minister and is already moving to fill the cabinet vacancies left by Boris Johnson and David Davis. "
                    "Government sources tell the paper that May has significant parliamentary support and that Brexiteers do not have the numbers to bring her down. "
                    "The Telegraph's political team judges that May will survive the immediate crisis, though her authority has been damaged."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Cabinet Meltdown Leaves May's Future Hanging by a Thread",
                "article_date": "2018-07-09",
                "article_summary": (
                    "The Times reports that Theresa May is facing the gravest crisis of her premiership after losing two of her most senior ministers within 24 hours. "
                    "The paper's political editor, citing Whitehall sources, says further ministerial resignations are expected and that May will be unable to hold her government together. "
                    "The Times characterises the situation as one from which no Prime Minister could reasonably be expected to recover."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK's May Under Pressure After Two Senior Ministers Quit Over Brexit Plan",
                "article_date": "2018-07-09",
                "article_summary": (
                    "Reuters reports that British Prime Minister Theresa May is under intensified political pressure following the resignations of Brexit Secretary David Davis and Foreign Secretary Boris Johnson over her Chequers blueprint. "
                    "The wire service notes that May still commands a working parliamentary majority and that a formal leadership challenge requires 48 Conservative MPs to submit letters of no confidence. "
                    "Reuters does not project an outcome, describing the political situation as fluid."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "May Faces Leadership Crisis After Double Resignation Blow",
                "article_date": "2018-07-09",
                "article_summary": (
                    "Sky News reports that Theresa May is in a 'full-blown leadership crisis' following the back-to-back resignations of David Davis and Boris Johnson. "
                    "Political correspondents say the resignations have fatally undermined May's ability to command her party, and that prominent backbenchers are gathering to discuss next steps. "
                    "Sky's live coverage describes the situation as 'potentially terminal' for May's premiership and predicts she cannot survive the week."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 32 — Jeremy Corbyn Survives Labour Parliamentary Party Coup 2016
    # -----------------------------------------------------------------------
    {
        "event_id": 32,
        "event_name": "Jeremy Corbyn Survives Labour Parliamentary Party Coup 2016",
        "event_date": "2016-07-20",
        "initial_coverage_date": "2016-06-27",
        "resolution_time_hours": 552,
        "event_category": "Resignation",
        "outcome": "Jeremy Corbyn refused to resign despite a vote of no confidence by Labour MPs, stood in the resulting leadership election, and won with an increased mandate of 61.8% in September 2016.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "Jeremy Corbyn is facing the gravest challenge to his Labour leadership after a cascade of shadow cabinet resignations in the days following the Brexit vote, with more than two dozen front-bench MPs having quit. "
            "The Parliamentary Labour Party is expected to pass a formal motion of no confidence and multiple potential challengers are being named. "
            "Corbyn insists he has a democratic mandate from party members and will not resign, but many Westminster observers believe the scale of the revolt makes his position impossible. "
            "The next weeks will determine whether Corbyn can hold together enough support among the wider Labour membership to withstand the parliamentary pressure."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "The Telegraph, Times, and Sky News all predicted Corbyn would be forced out, severely underestimating his grassroots membership strength; this event tests whether outlets systematically misjudged the Labour membership base versus the parliamentary party."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Corbyn's Grassroots Support May Be Enough to Defy Parliamentary Pressure",
                "article_date": "2016-06-27",
                "article_summary": (
                    "The Guardian reports that Jeremy Corbyn is defying calls to resign and that his support among Labour's wider membership may be sufficient to survive any formal leadership challenge. "
                    "The paper speaks to Momentum organisers who say Corbyn commands strong grassroots loyalty entirely unrepresented in the parliamentary party. "
                    "The Guardian's political editor frames his refusal to resign as a potentially sustainable position, suggesting Corbyn could win a membership ballot if one is forced."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Labour Crisis: What Happens if MPs Vote No Confidence in Corbyn?",
                "article_date": "2016-06-27",
                "article_summary": (
                    "The BBC explains the constitutional and procedural implications of the Labour parliamentary party's planned no-confidence vote, noting that the result is not legally binding on the leader. "
                    "Political correspondents report that the PLP is expected to vote heavily against Corbyn but that his fate depends partly on whether he chooses to trigger a membership ballot. "
                    "The BBC presents the situation as genuinely uncertain, with analysts suggesting Corbyn retains strong grassroots support that complicates the path to removing him."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Corbyn Cannot Survive: Labour MPs Move to Force Out Leader After Brexit Chaos",
                "article_date": "2016-06-27",
                "article_summary": (
                    "The Telegraph reports that Labour MPs are confident they can force Jeremy Corbyn from the leadership following the catastrophic no-confidence vote expected this week. "
                    "Senior Labour figures tell the paper that Corbyn's position will become untenable once he faces a formal parliamentary vote, and that he will stand down rather than face a humiliating membership contest. "
                    "The Telegraph's political team judges that Corbyn's leadership is effectively over."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Corbyn's Labour Leadership Is Over, Senior MPs Declare",
                "article_date": "2016-06-27",
                "article_summary": (
                    "The Times reports that Labour MPs are certain Corbyn will resign before being formally removed, with multiple senior figures telling the paper he will not risk the indignity of a contested leadership election. "
                    "The paper's political correspondent quotes a shadow cabinet member saying Corbyn has privately acknowledged he may have no choice but to go. "
                    "The Times frames this as the final chapter of Corbyn's leadership, predicting his departure before the week is out."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Labour Party Plunges Into Leadership Crisis After Brexit Vote",
                "article_date": "2016-06-27",
                "article_summary": (
                    "Reuters reports that Britain's Labour Party is in acute crisis following mass shadow cabinet resignations, with Jeremy Corbyn under pressure to stand down from the leadership. "
                    "The wire service notes that Corbyn has declined to resign despite demands from MPs and that under party rules a leadership contest would require either his resignation or a successful challenge obtaining sufficient nominations. "
                    "Reuters presents no outcome projection, describing the situation as politically fluid."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Corbyn Will Be Gone Within Days, Labour Insiders Say",
                "article_date": "2016-06-27",
                "article_summary": (
                    "Sky News reports that senior Labour figures believe Jeremy Corbyn will resign within days, unable to hold together a front bench or win a confidence vote. "
                    "Sky's parliamentary reporter says the scale of the revolt makes Corbyn's continued leadership 'impossible in practice', and that even allies are privately telling him he cannot survive. "
                    "Sky explicitly predicts Corbyn will announce his resignation before the end of the week."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 34 — Jeremy Corbyn Wins Labour Leadership Against Owen Smith September 2016
    # -----------------------------------------------------------------------
    {
        "event_id": 34,
        "event_name": "Jeremy Corbyn Wins Labour Leadership Against Owen Smith September 2016",
        "event_date": "2016-09-24",
        "initial_coverage_date": "2016-09-01",
        "resolution_time_hours": 552,
        "event_category": "Vote_Confidence",
        "outcome": "Jeremy Corbyn won the Labour leadership ballot against Owen Smith with 61.8% of the vote, confounding predictions that the challenge would succeed or produce a dramatically close result.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "Jeremy Corbyn is facing a formal leadership challenge from Owen Smith following the no-confidence vote passed by Labour MPs in June, triggered by the post-Brexit shadow cabinet resignations. "
            "Smith has been making a strong campaign on a platform of electability, and several polls of Labour members suggest the race may be closer than Corbyn's team publicly acknowledges. "
            "The result of the membership ballot will be announced later this month at a special Labour conference in Liverpool. "
            "Commentators are divided on whether Corbyn's grassroots organisational strength can withstand the professional campaign being run by the Smith camp."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "The Telegraph and Times both predicted Owen Smith would defeat or come very close to defeating Corbyn, severely underestimating the scale of Corbyn's membership support; the Guardian correctly predicted Corbyn's renewed mandate."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Corbyn's Grassroots Machine Could Deliver a Bigger Win Than Expected",
                "article_date": "2016-09-01",
                "article_summary": (
                    "The Guardian reports that Jeremy Corbyn's campaign team is quietly confident of winning the Labour leadership election with a larger share than many Westminster commentators expect. "
                    "The paper speaks to Momentum organisers who say the flow of new members, many of whom joined to support Corbyn, gives him a structural advantage that polling of existing members undercounts. "
                    "The Guardian characterises Smith's challenge as credible but insufficient to overcome Corbyn's organisational base."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Labour Leadership: Corbyn and Smith Head for Conference Showdown",
                "article_date": "2016-09-01",
                "article_summary": (
                    "The BBC examines the state of the Labour leadership contest as ballots are returned, with political correspondents noting that polling of Labour members shows a Corbyn lead but with significant uncertainty. "
                    "BBC analysis suggests that while Corbyn is favoured, the Smith campaign's targeting of moderate members could tighten the result considerably. "
                    "The BBC does not project a winner, noting that previous YouGov polling may not capture the full picture of an expanded membership."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Smith Closing the Gap as Labour Members Waver Over Corbyn's Electability",
                "article_date": "2016-09-01",
                "article_summary": (
                    "The Telegraph reports that Owen Smith is closing the gap on Jeremy Corbyn in the Labour leadership contest, with the paper's analysis suggesting Smith could win or force a dramatically close result. "
                    "The paper quotes Labour moderate MPs who say their private canvassing of members suggests Smith is performing better than public polls indicate. "
                    "The Telegraph predicts a much closer result than Corbyn's team acknowledges, with Smith positioned to cause a significant upset."
                ),
                "framing_prediction": "WILL_LOSE",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Smith on Course to Spring Leadership Surprise, Poll Analysis Suggests",
                "article_date": "2016-09-01",
                "article_summary": (
                    "The Times reports that private polling commissioned by Owen Smith's campaign suggests he may be within striking distance of defeating Jeremy Corbyn in the Labour leadership ballot. "
                    "The paper's political correspondent cites signals from within the membership that electability concerns are weighing more heavily than early polling suggested. "
                    "The Times predicts a significantly closer result than a Corbyn landslide, with Smith capable of winning a majority of eligible Labour members."
                ),
                "framing_prediction": "WILL_LOSE",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "Britain's Labour Faces Verdict on Corbyn Leadership in Membership Ballot",
                "article_date": "2016-09-01",
                "article_summary": (
                    "Reuters reports that Britain's Labour Party is awaiting the results of its leadership ballot, with Jeremy Corbyn and challenger Owen Smith having made their final pitches to the membership. "
                    "The wire service notes that polls of Labour members consistently show Corbyn ahead but that turnout patterns and inclusion of newly registered members introduce uncertainty. "
                    "Reuters does not project an outcome, reporting both candidates claim confidence in their respective positions."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Labour Leadership: Is This Really as Close as Some Are Claiming?",
                "article_date": "2016-09-01",
                "article_summary": (
                    "Sky News examines claims from Owen Smith's campaign that the Labour leadership result will be much closer than public polling suggests. "
                    "Sky's political correspondent says the independent polling evidence still points to a Corbyn victory but that Smith's campaign has professionalised and has genuine grassroots support in some regions. "
                    "Sky frames the outcome as uncertain, suggesting Smith has mounted a better challenge than initially expected."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 35 — George Osborne Reverses Tax Credits Cuts in Autumn Statement 2015
    # -----------------------------------------------------------------------
    {
        "event_id": 35,
        "event_name": "George Osborne Reverses Tax Credits Cuts in Autumn Statement 2015",
        "event_date": "2015-11-25",
        "initial_coverage_date": "2015-10-27",
        "resolution_time_hours": 696,
        "event_category": "Economic_Policy",
        "outcome": "George Osborne reversed his planned cuts to working tax credits in the Autumn Statement, abandoning the policy entirely after losing the Lords vote and facing sustained pressure from Conservative MPs in marginal seats.",
        "outcome_binary": "REVERSED",
        "event_description": (
            "The House of Lords voted last night to delay the government's planned cuts to working tax credits, passing a fatal motion against the statutory instrument that would have reduced the income threshold from £6,420 to £3,850. "
            "Osborne faces a constitutional conflict with the Lords and a politically toxic backlash from Conservative MPs who fear the impact on low-income constituents. "
            "Government sources insist the Chancellor intends to press ahead with the welfare savings, and ministers are exploring legal routes to override or circumvent the Lords vote. "
            "The Autumn Statement in late November is now seen as the critical moment when Osborne must decide how to proceed."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "The Telegraph, Times, and Sky News predicted Osborne would find a way to implement the cuts, while the Guardian correctly anticipated a full U-turn; this event tests whether pro-government outlets systematically under-predicted Conservative retreats on austerity measures."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Osborne May Be Forced Into Tax Credits Climbdown, Treasury Sources Hint",
                "article_date": "2015-10-27",
                "article_summary": (
                    "The Guardian reports that Treasury sources have privately acknowledged to the paper that a full reversal of the tax credits cuts is now possible, amid mounting political pressure from Conservative backbenchers. "
                    "The paper notes that the combination of the Lords vote and internal Tory dissent has created conditions where pressing ahead could prove more politically costly than retreating. "
                    "The Guardian frames a U-turn as the most likely outcome if Osborne is to avoid open rebellion at the Autumn Statement."
                ),
                "framing_prediction": "WILL_UTURN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Tax Credits Row: What Happens Now After Lords Defeat?",
                "article_date": "2015-10-27",
                "article_summary": (
                    "The BBC outlines the political and constitutional options facing George Osborne after the House of Lords voted against the tax credits cuts statutory instrument. "
                    "Political correspondents note that Osborne could choose to modify, delay, or withdraw the cuts, or challenge the Lords' powers, with each option carrying significant political risk. "
                    "The BBC presents the Autumn Statement as the likely decision point but does not project which path Osborne will take."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Osborne Will Not Bow to Lords Pressure on Tax Credits, Treasury Says",
                "article_date": "2015-10-27",
                "article_summary": (
                    "The Telegraph reports that Number 11 has made clear to the paper that George Osborne will not reverse course on tax credits despite the Lords vote, which the government views as a constitutional overreach. "
                    "The paper says Osborne intends to use the Autumn Statement to announce transitional arrangements, not a retreat, and that the welfare savings remain central to his fiscal plan. "
                    "The Telegraph judges that the Chancellor's political credibility depends on holding the line and that he will find a way to implement the cuts."
                ),
                "framing_prediction": "WILL_PASS",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Chancellor Determined to Find Way Through on Tax Credits Despite Lords Setback",
                "article_date": "2015-10-27",
                "article_summary": (
                    "The Times reports that George Osborne remains committed to delivering the welfare savings from tax credit cuts and is exploring options to proceed despite the Lords vote. "
                    "The paper's Westminster correspondent says Osborne views backing down as politically impossible given his stated fiscal targets, and that the Treasury is working on a modified package achieving equivalent savings. "
                    "The Times predicts that Osborne will announce some form of the cuts at the Autumn Statement, possibly with transitional protection but without abandoning the core policy."
                ),
                "framing_prediction": "WILL_PASS",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Government Reviews Tax Credits Plans After House of Lords Defeat",
                "article_date": "2015-10-27",
                "article_summary": (
                    "Reuters reports that the British government is reviewing its options on planned cuts to working tax credits after the House of Lords voted against the statutory instrument implementing them. "
                    "The wire service notes that Chancellor Osborne has reaffirmed his commitment to welfare savings but that pressure from Conservative MPs in marginal seats is complicating the path forward. "
                    "Reuters does not forecast whether Osborne will press ahead or reverse the policy, noting the Autumn Statement will clarify the government's intentions."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Tax Credits Battle: Osborne Stands Firm Despite Lords Rebellion",
                "article_date": "2015-10-27",
                "article_summary": (
                    "Sky News reports that George Osborne has told colleagues he intends to implement the tax credits cuts through alternative means, dismissing the Lords vote as an illegitimate intervention in financial matters. "
                    "Sky's political correspondent says government sources are confident the Chancellor will find a path forward at the Autumn Statement that delivers the planned welfare savings. "
                    "Sky frames Osborne as unlikely to U-turn, citing his track record of delivering on fiscal commitments even under political pressure."
                ),
                "framing_prediction": "WILL_PASS",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 37 — 2015 UK General Election: Conservatives Win Unexpected Majority
    # -----------------------------------------------------------------------
    {
        "event_id": 37,
        "event_name": "2015 UK General Election – Conservatives Win Unexpected Majority",
        "event_date": "2015-05-08",
        "initial_coverage_date": "2015-05-04",
        "resolution_time_hours": 96,
        "event_category": "Election_Leadership",
        "outcome": "The Conservatives won an outright majority of 331 seats, defying unanimous pre-election polling that had projected a hung parliament and denying Labour any path to government.",
        "outcome_binary": "WON",
        "event_description": (
            "With three days until polling day, every published poll shows the Conservatives and Labour tied within the margin of error, pointing overwhelmingly to a hung parliament. "
            "Commentators are focused on coalition arithmetic rather than outright majority scenarios, with the SNP expected to hold the balance of power in any minority government arrangement. "
            "Conservative campaign strategists are publicly acknowledging they cannot win a majority, while Labour sources express cautious optimism about forming a minority government. "
            "The Lib Dems are forecast to lose many of their 57 seats but retain enough to be potential coalition partners for either main party."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "The Guardian, Times, and Sky News all projected a hung parliament with Labour potentially forming a government, when in reality the Conservatives won a majority of 331 seats; this event is central to understanding how outlets systematically under-predicted Conservative strength in 2015."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Final Polls Point to Hung Parliament With No Clear Path to Majority for Either Party",
                "article_date": "2015-05-04",
                "article_summary": (
                    "The Guardian reports that the final polls before Thursday's general election show the Conservatives and Labour neck-and-neck on around 33-34%, making an outright majority for either side virtually impossible. "
                    "The paper's analysis focuses on coalition scenarios, exploring how a Labour minority government supported by the SNP might work in practice. "
                    "The Guardian concludes that the most likely outcome is a hung parliament, with Ed Miliband having a plausible path to Downing Street."
                ),
                "framing_prediction": "WILL_LOSE",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Election 2015: Polls Point to Knife-Edge Result With No Party Close to Majority",
                "article_date": "2015-05-04",
                "article_summary": (
                    "The BBC presents a comprehensive breakdown of the final pre-election polling, with all major surveys showing a dead heat between the Conservatives and Labour. "
                    "Political analysts on the BBC note that the polls have been consistent throughout the campaign and that a hung parliament appears the almost certain outcome. "
                    "The BBC's own experts acknowledge that constituency-level modelling creates some uncertainty but present the consensus view of no overall majority for either party."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Don't Write Off a Tory Majority: Why the Polls May Be Underestimating Cameron",
                "article_date": "2015-05-04",
                "article_summary": (
                    "The Telegraph argues that the published polls may be systematically under-measuring Conservative support due to a repeat of the 'shy Tory' effect that distorted predictions in 1992. "
                    "The paper's lead columnist contends that Cameron's personal approval ratings outstrip those of Ed Miliband and that economic competence polling favours the Conservatives, creating conditions for an outperformance on polling day. "
                    "The Telegraph predicts the Conservatives will outperform the polls and may secure enough seats to govern without a coalition partner."
                ),
                "framing_prediction": "WILL_WIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Election 2015 Final Verdict: Coalition Negotiations Will Begin on Friday Morning",
                "article_date": "2015-05-04",
                "article_summary": (
                    "The Times projects with confidence that no party will win an outright majority on Thursday, setting out the terms of likely coalition negotiations in detail. "
                    "The paper's political team has modelled hundreds of seat scenarios and concludes that a Conservative majority is 'essentially ruled out' by the uniform polling evidence. "
                    "The Times predicts the most likely outcome is a Conservative-led minority government dependent on Lib Dem or DUP support, with Ed Miliband also having a route to power."
                ),
                "framing_prediction": "WILL_LOSE",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Election Too Close to Call as Final Polls Show Dead Heat",
                "article_date": "2015-05-04",
                "article_summary": (
                    "Reuters reports that Britain's general election on Thursday is too close to call, with all final polls showing the Conservatives and Labour within the margin of error at around 33-34% each. "
                    "The wire service notes that the uniform polling consensus points strongly to a hung parliament and that post-election coalition negotiations are expected to determine who governs. "
                    "Reuters does not project a winner, reflecting the near-universal polling uncertainty."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Election 2015: No Winner in Sight as Final Polls Show Deadlock",
                "article_date": "2015-05-04",
                "article_summary": (
                    "Sky News reports that its final poll of polls shows the Conservatives and Labour deadlocked, making a hung parliament the overwhelming probability according to seat projection models. "
                    "Sky's political team focuses on coalition and confidence-and-supply arithmetic, interviewing SNP, Lib Dem, and DUP representatives about post-election negotiations. "
                    "Sky frames the election as one where no single party will command a majority, and neither leader will walk straight into Downing Street on Friday morning."
                ),
                "framing_prediction": "WILL_LOSE",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 38 — EU Referendum (Brexit) June 2016: Leave Wins Against Expectations
    # -----------------------------------------------------------------------
    {
        "event_id": 38,
        "event_name": "EU Referendum June 2016-Leave Wins",
        "event_date": "2016-06-23",
        "initial_coverage_date": "2016-06-19",
        "resolution_time_hours": 96,
        "event_category": "Election_Leadership",
        "outcome": "The United Kingdom voted to leave the European Union by 51.9% to 48.1%, defying betting markets and most published forecasts that had pointed to a narrow Remain victory.",
        "outcome_binary": "LEAVE",
        "event_description": (
            "With days until the referendum, betting markets price a Remain victory at around 80-85% probability, "
            "and the weight of published commentary anticipates that undecided voters will break for the status quo. "
            "Final polls are mixed and close, with several phone polls showing a narrow Remain lead and online polls showing a dead heat. "
            "Sterling has strengthened on the assumption of a Remain win, and most outlets are framing the likely result as a narrow victory for staying in the EU."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A landmark surprise outcome: Guardian, Times and Sky News all leaned toward a narrow Remain win (FALSE), "
            "while the Telegraph's pro-Leave framing predicted the actual result (TRUE) and BBC/Reuters stayed UNCLEAR. "
            "Central to the FALSE class — a case where consensus forecasting failed badly."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Final Polls Suggest Remain Will Edge a Narrow Referendum Victory",
                "article_date": "2016-06-19",
                "article_summary": (
                    "The Guardian reports that the balance of final polling and the historic tendency of undecided voters to favour the status quo point to a narrow Remain victory. "
                    "The paper's analysis emphasises that betting markets have moved decisively toward Remain and that economic-risk messaging appears to be landing with wavering voters. "
                    "The Guardian concludes that the UK is most likely to vote to stay in the European Union, albeit by a slim margin."
                ),
                "framing_prediction": "WILL_REMAIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "EU Referendum: Polls Remain Too Close to Call as Campaign Enters Final Days",
                "article_date": "2016-06-19",
                "article_summary": (
                    "The BBC presents the final-week polling as genuinely too close to call, noting the divergence between phone polls leaning Remain and online polls showing a dead heat. "
                    "Its analysts stress that turnout among different demographics could prove decisive and decline to forecast a winner. "
                    "The BBC frames the outcome as uncertain, with both campaigns claiming momentum."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Don't Be Surprised if Britain Votes to Leave: The Polls May Be Understating Leave",
                "article_date": "2016-06-19",
                "article_summary": (
                    "The Telegraph argues that the published polls and complacent betting markets may be significantly understating the strength of the Leave vote, particularly among older and working-class voters likely to turn out in force. "
                    "The paper contends that immigration and sovereignty concerns are more salient than economic-risk warnings, and that turnout patterns favour Leave. "
                    "The Telegraph predicts a genuine possibility of a Leave victory on referendum day."
                ),
                "framing_prediction": "WILL_LEAVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Remain on Course for Narrow Win as Markets Price In Status Quo",
                "article_date": "2016-06-19",
                "article_summary": (
                    "The Times reports that financial markets and the bulk of final polling point to a narrow win for Remain, with sterling strengthening on growing confidence the UK will stay in the EU. "
                    "The paper's political team judges that late-deciding voters are likely to opt for the safer option in the polling booth. "
                    "The Times concludes that Remain is the more probable outcome, while cautioning the margin will be tight."
                ),
                "framing_prediction": "WILL_REMAIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Heads to EU Referendum With Polls Showing No Clear Lead",
                "article_date": "2016-06-19",
                "article_summary": (
                    "Reuters reports that Britain enters its EU referendum with final polls showing no clear lead, the contest balanced within the margin of error. "
                    "The wire service notes that bookmakers favour Remain but that pollsters have warned the result is highly uncertain and turnout-dependent. "
                    "Reuters makes no projection, reflecting the genuine uncertainty in the data."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Remain Set to Win Narrowly, Final Poll of Polls Suggests",
                "article_date": "2016-06-19",
                "article_summary": (
                    "Sky News reports that its final aggregation of polling gives Remain a slender lead, with its analysts suggesting risk-averse undecided voters will tip the balance toward staying in the EU. "
                    "Sky's coverage highlights market confidence and the established pattern of status-quo votes outperforming on the day. "
                    "Sky concludes that a narrow Remain victory is the most likely result."
                ),
                "framing_prediction": "WILL_REMAIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 40 — North Shropshire By-election December 2021: Lib Dem Upset
    # -----------------------------------------------------------------------
    {
        "event_id": 40,
        "event_name": "North Shropshire By-election December 2021 – Lib Dem Gain",
        "event_date": "2021-12-16",
        "initial_coverage_date": "2021-12-13",
        "resolution_time_hours": 72,
        "event_category": "Election_Leadership",
        "outcome": "The Liberal Democrats overturned a Conservative majority of nearly 23,000 to win North Shropshire, a seat held by the Conservatives and their predecessors for almost two centuries.",
        "outcome_binary": "LIB_DEM_GAIN",
        "event_description": (
            "The by-election, triggered by Owen Paterson's resignation amid a lobbying scandal, takes place against the backdrop of mounting Partygate revelations damaging the Conservatives nationally. "
            "The seat has been Conservative-held for generations with a majority approaching 23,000, and the party is defending on traditionally safe rural territory. "
            "While the Liberal Democrats are mounting an energetic campaign and tactical voting is being urged, the scale of the majority leads much of the press to expect the Conservatives to hold on, even if with a sharply reduced margin."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A by-election shock: Guardian, Times and Telegraph expected a Conservative hold despite pressure (FALSE), "
            "Sky News read the Lib Dem surge correctly (TRUE), and BBC/Reuters hedged (PARTIAL). Adds FALSE labels with strong source divergence."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Conservatives Expected to Cling On in North Shropshire Despite Partygate Anger",
                "article_date": "2021-12-13",
                "article_summary": (
                    "The Guardian reports that, although Partygate revelations have damaged the Conservatives, the sheer size of the 23,000 majority means the party is still expected to hold North Shropshire, albeit with a much-reduced margin. "
                    "The paper notes Liberal Democrat optimism and tactical-voting appeals but judges that overturning such a majority would be historically rare. "
                    "The Guardian frames a narrow Conservative hold as the most likely outcome."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "North Shropshire By-election: Conservatives Face Tough Test Amid Scandal",
                "article_date": "2021-12-13",
                "article_summary": (
                    "The BBC reports that the Conservatives face a difficult by-election test in North Shropshire, with the Liberal Democrats hopeful and the national mood turning against the government. "
                    "Its analysts note the size of the majority makes a Conservative loss unlikely but not impossible given the circumstances. "
                    "The BBC declines to forecast a winner, framing the contest as unpredictable."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Tories Braced for Reduced Majority but Expected to Hold North Shropshire",
                "article_date": "2021-12-13",
                "article_summary": (
                    "The Telegraph reports that Conservative strategists expect to hold North Shropshire despite the damage from the Paterson affair and Partygate, citing the depth of the party's historic support in the rural seat. "
                    "The paper frames the contest as a protest-vote test the Conservatives should survive. "
                    "The Telegraph predicts a Conservative hold on a reduced majority."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Conservatives Tipped to Survive North Shropshire Test Despite Anger",
                "article_date": "2021-12-13",
                "article_summary": (
                    "The Times reports that, while the by-election will be uncomfortable for the Conservatives, the party is tipped to survive given a majority approaching 23,000 and the absence of a single dominant challenger in most analyses. "
                    "The paper notes the Liberal Democrats' targeting operation but judges the mountain too steep to climb. "
                    "The Times predicts a Conservative hold."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Johnson Faces By-election Test in Traditionally Safe Seat",
                "article_date": "2021-12-13",
                "article_summary": (
                    "Reuters reports that Boris Johnson faces a by-election test in the traditionally safe Conservative seat of North Shropshire amid a deepening Partygate controversy. "
                    "The wire service notes both Conservative defensiveness and Liberal Democrat hopes without projecting a result. "
                    "Reuters frames the outcome as a barometer of Johnson's standing but makes no prediction."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Lib Dems Sense Historic Upset in North Shropshire as Tory Vote Collapses",
                "article_date": "2021-12-13",
                "article_summary": (
                    "Sky News reports that Liberal Democrat campaigners and several local canvassing returns suggest a genuine chance of a historic upset, with the Conservative vote collapsing under the weight of Partygate and the Paterson affair. "
                    "Sky's political team highlights tactical voting by Labour supporters coalescing behind the Liberal Democrats. "
                    "Sky frames a Liberal Democrat victory as a real possibility rather than a remote one."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 41 — Copeland By-election February 2017: Conservative Gain
    # -----------------------------------------------------------------------
    {
        "event_id": 41,
        "event_name": "Copeland By-election February 2017 – Conservative Gain",
        "event_date": "2017-02-23",
        "initial_coverage_date": "2017-02-20",
        "resolution_time_hours": 72,
        "event_category": "Election_Leadership",
        "outcome": "The Conservatives gained Copeland from Labour — the first by-election gain by a governing party from the main opposition since 1982 — overturning a seat Labour had held since 1935.",
        "outcome_binary": "CON_GAIN",
        "event_description": (
            "The by-election in Copeland, a seat Labour has held since 1935, takes place amid questions over Jeremy Corbyn's leadership and Labour's position on the local nuclear industry. "
            "Although Labour's majority had narrowed at the 2015 election, the historic pattern of governing parties losing — not gaining — by-election seats leads much of the press to expect Labour to hold on, even if narrowly. "
            "The Conservatives are campaigning hard on the nuclear issue, but a governing-party gain would be almost without modern precedent."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A rare governing-party by-election gain that confounded the historic precedent most outlets relied on. "
            "Guardian, Times and Sky News expected a narrow Labour hold (FALSE); Telegraph read the Conservative momentum (TRUE); BBC/Reuters hedged (PARTIAL)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Labour Expected to Hold Copeland Despite Corbyn Leadership Doubts",
                "article_date": "2017-02-20",
                "article_summary": (
                    "The Guardian reports that, despite doubts over Jeremy Corbyn's leadership and local anxiety about Labour's nuclear stance, the party is expected to hold Copeland given its unbroken tenure since 1935. "
                    "The paper notes that governing parties almost never gain seats in by-elections, which works in Labour's favour. "
                    "The Guardian frames a narrow Labour hold as the likeliest result."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Copeland By-election: Labour Faces Tight Contest in Long-held Seat",
                "article_date": "2017-02-20",
                "article_summary": (
                    "The BBC reports that Labour faces an unexpectedly tight contest in Copeland, a seat it has held for more than 80 years, amid the nuclear-industry debate and leadership questions. "
                    "Its analysts note the historic rarity of a governing-party gain while acknowledging Conservative confidence. "
                    "The BBC declines to forecast the result, framing it as closely fought."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Conservatives Sense Historic Copeland Win as Corbyn's Labour Falters",
                "article_date": "2017-02-20",
                "article_summary": (
                    "The Telegraph reports that Conservative campaigners sense a historic by-election gain in Copeland, citing local support for the nuclear industry and deep voter unease with Jeremy Corbyn's leadership. "
                    "The paper frames the contest as a chance for the governing party to defy precedent and seize a long-held Labour seat. "
                    "The Telegraph predicts a Conservative gain."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Labour Tipped to Survive Copeland Scare in Heartland Seat",
                "article_date": "2017-02-20",
                "article_summary": (
                    "The Times reports that, while Copeland will be close, Labour is tipped to survive the scare and hold a seat it has occupied since 1935. "
                    "The paper notes that governing parties rarely overturn opposition seats and that local Labour organisation should prove decisive. "
                    "The Times predicts a narrow Labour hold."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Labour Faces By-election Tests in Copeland and Stoke",
                "article_date": "2017-02-20",
                "article_summary": (
                    "Reuters reports that Labour faces twin by-election tests in Copeland and Stoke-on-Trent Central that will be read as verdicts on Jeremy Corbyn's leadership. "
                    "The wire service notes Conservative optimism in Copeland and the historic difficulty of a governing-party gain, without projecting a winner. "
                    "Reuters makes no forecast."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Labour Braced but Expected to Hold Copeland in Corbyn Leadership Test",
                "article_date": "2017-02-20",
                "article_summary": (
                    "Sky News reports that Labour is braced for a difficult night but is still expected to hold Copeland, with its analysts citing the seat's long Labour history and the rarity of governing-party by-election gains. "
                    "Sky frames the contest as a test Corbyn's Labour should narrowly pass. "
                    "Sky predicts a Labour hold."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 42 — Peterborough By-election June 2019: Labour Holds Off Brexit Party
    # -----------------------------------------------------------------------
    {
        "event_id": 42,
        "event_name": "Peterborough By-election June 2019 – Labour Hold",
        "event_date": "2019-06-06",
        "initial_coverage_date": "2019-06-03",
        "resolution_time_hours": 72,
        "event_category": "Election_Leadership",
        "outcome": "Labour held Peterborough, defeating the Brexit Party by around 700 votes, despite widespread expectations that Nigel Farage's newly dominant party would win its first Commons seat.",
        "outcome_binary": "LAB_HOLD",
        "event_description": (
            "The by-election follows the Brexit Party's commanding victory in the European Parliament elections weeks earlier, when it topped the national poll. "
            "Peterborough is seen as fertile territory: a Leave-voting marginal where the new party hopes to win its first Westminster seat. "
            "Much of the press expects the Brexit Party to capitalise on its momentum and the collapse of the Conservative vote, framing a Brexit Party gain as the likely headline result."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A surprise Labour hold against the expected Brexit Party surge. Guardian, Times, Telegraph and Sky News all anticipated a Brexit Party win (FALSE); "
            "BBC and Reuters hedged (PARTIAL). The single highest-FALSE event in the additions (4 FALSE)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Brexit Party Poised to Win First MP as Peterborough Goes to the Polls",
                "article_date": "2019-06-03",
                "article_summary": (
                    "The Guardian reports that the Brexit Party is poised to win its first seat in the Commons in Peterborough, riding the momentum of its European election triumph and the collapse of the Conservative vote. "
                    "The paper notes Labour's difficulties over Brexit and antisemitism but judges the new party's surge difficult to resist in a Leave-voting marginal. "
                    "The Guardian frames a Brexit Party gain as the most likely outcome."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Peterborough By-election: Brexit Party Hopes to Win First Seat",
                "article_date": "2019-06-03",
                "article_summary": (
                    "The BBC reports that the Brexit Party hopes to convert its European election success into its first Westminster seat in Peterborough, in a contest seen as a barometer of post-EU-election politics. "
                    "Its analysts note Labour's organisational strength and a large postal vote as factors that could complicate the picture. "
                    "The BBC declines to forecast a winner."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Farage's Brexit Party on Course to Seize Peterborough from Labour",
                "article_date": "2019-06-03",
                "article_summary": (
                    "The Telegraph reports that Nigel Farage's Brexit Party is on course to seize Peterborough from Labour, citing the party's commanding European-election performance and the disaffection of Leave voters with both main parties. "
                    "The paper frames the by-election as the launchpad for a Brexit Party Westminster breakthrough. "
                    "The Telegraph predicts a Brexit Party gain."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Brexit Party Favourite to Win Peterborough as Labour Vote Wavers",
                "article_date": "2019-06-03",
                "article_summary": (
                    "The Times reports that the Brexit Party is the clear favourite to win Peterborough, with its analysts judging that the European-election surge and Conservative collapse hand Farage's party the advantage. "
                    "The paper notes Labour's recall-petition origins to the by-election and its wavering vote in a Leave-leaning seat. "
                    "The Times predicts a Brexit Party victory."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK's Brexit Party Eyes First Parliamentary Seat in Peterborough Vote",
                "article_date": "2019-06-03",
                "article_summary": (
                    "Reuters reports that the Brexit Party is eyeing its first parliamentary seat in the Peterborough by-election, weeks after topping the European elections. "
                    "The wire service notes the contest is being watched as a test of the party's staying power, while Labour fights to retain the marginal. "
                    "Reuters makes no projection of the result."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Brexit Party Set for Breakthrough Win in Peterborough, Analysts Say",
                "article_date": "2019-06-03",
                "article_summary": (
                    "Sky News reports that analysts expect the Brexit Party to achieve a breakthrough win in Peterborough, translating its European-election momentum into a first Commons seat. "
                    "Sky's political team highlights the fragmentation of the two main parties' vote in a Leave-voting marginal. "
                    "Sky predicts a Brexit Party gain."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 43 — Tiverton & Honiton By-election June 2022: Lib Dem Upset
    # -----------------------------------------------------------------------
    {
        "event_id": 43,
        "event_name": "Tiverton & Honiton By-election June 2022 – Lib Dem Gain",
        "event_date": "2022-06-23",
        "initial_coverage_date": "2022-06-20",
        "resolution_time_hours": 72,
        "event_category": "Election_Leadership",
        "outcome": "The Liberal Democrats overturned a Conservative majority of more than 24,000 to win Tiverton & Honiton, recording one of the largest majorities overturned in British by-election history.",
        "outcome_binary": "LIB_DEM_GAIN",
        "event_description": (
            "The by-election, caused by the resignation of the Conservative MP after a misconduct scandal, takes place amid sustained Partygate fallout and economic pressure on the government. "
            "The Conservatives are defending a majority exceeding 24,000 in a long-held rural South West seat. "
            "Although the Liberal Democrats are mounting a strong tactical-voting campaign, the size of the majority leads several outlets to expect the Conservatives to hold on despite the national headwinds."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A record-breaking by-election upset. Guardian, Times and Telegraph expected a Conservative hold given the 24,000 majority (FALSE); "
            "Sky News read the Lib Dem surge (TRUE); BBC/Reuters hedged (PARTIAL)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Conservatives Expected to Hold Tiverton Despite Partygate Damage",
                "article_date": "2022-06-20",
                "article_summary": (
                    "The Guardian reports that, although the government is battered by Partygate and the cost-of-living crisis, the Conservatives are expected to hold Tiverton & Honiton given a majority of more than 24,000. "
                    "The paper notes Liberal Democrat optimism and tactical voting but judges that overturning so vast a majority would be historically extraordinary. "
                    "The Guardian frames a Conservative hold as the most probable result."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Tiverton & Honiton: Conservatives Defend Huge Majority Amid Difficult Night",
                "article_date": "2022-06-20",
                "article_summary": (
                    "The BBC reports that the Conservatives are defending a substantial majority in Tiverton & Honiton on what is expected to be a difficult by-election night for the government. "
                    "Its analysts note that the scale of the majority makes a loss historically unlikely, while acknowledging the Liberal Democrats' targeting effort. "
                    "The BBC declines to forecast a result."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Tories Expected to Cling On in Tiverton Despite National Turmoil",
                "article_date": "2022-06-20",
                "article_summary": (
                    "The Telegraph reports that Conservative campaigners expect to cling on in Tiverton & Honiton despite national turmoil, pointing to the depth of the party's support across the rural Devon seat. "
                    "The paper frames a Liberal Democrat win as requiring an almost unprecedented swing. "
                    "The Telegraph predicts a Conservative hold."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Conservatives Tipped to Survive Tiverton Test on Vast Majority",
                "article_date": "2022-06-20",
                "article_summary": (
                    "The Times reports that, while uncomfortable, the Tiverton & Honiton by-election should see the Conservatives survive on the strength of a majority exceeding 24,000. "
                    "The paper notes the Liberal Democrats' history of by-election upsets but judges this majority a bridge too far. "
                    "The Times predicts a Conservative hold."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM Johnson Faces Twin By-election Tests After Partygate",
                "article_date": "2022-06-20",
                "article_summary": (
                    "Reuters reports that Boris Johnson faces twin by-election tests, including in Tiverton & Honiton, seen as a verdict on his leadership after Partygate. "
                    "The wire service notes the size of the Conservative majority alongside Liberal Democrat hopes, without projecting an outcome. "
                    "Reuters makes no forecast."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Lib Dems on Course for Stunning Tiverton Upset, Canvass Returns Suggest",
                "article_date": "2022-06-20",
                "article_summary": (
                    "Sky News reports that Liberal Democrat canvass returns and local momentum point to a stunning upset in Tiverton & Honiton, with the Conservative vote collapsing under the weight of Partygate and economic anger. "
                    "Sky's political team highlights coordinated tactical voting behind the Liberal Democrats. "
                    "Sky frames a Liberal Democrat gain as the likely outcome despite the huge majority."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 44 — Prorogation Supreme Court Ruling September 2019: Government Defeated
    # -----------------------------------------------------------------------
    {
        "event_id": 44,
        "event_name": "Prorogation Supreme Court Ruling September 2019 – Government Defeated",
        "event_date": "2019-09-24",
        "initial_coverage_date": "2019-09-20",
        "resolution_time_hours": 96,
        "event_category": "Legal_Courts",
        "outcome": "The Supreme Court ruled unanimously that Boris Johnson's prorogation of Parliament was unlawful, void and of no effect — a decisive defeat for the government that few had predicted would be so absolute.",
        "outcome_binary": "GOV_LOST",
        "event_description": (
            "The Supreme Court is hearing appeals over whether Boris Johnson's five-week prorogation of Parliament was lawful, after lower courts split: the English High Court found the matter non-justiciable, while Scotland's Court of Session ruled the prorogation unlawful. "
            "Government lawyers argue prorogation is an inherently political act beyond the reach of the courts. "
            "With the legal establishment divided and the High Court having sided with the government, much commentary anticipates either a government win or a narrow, equivocal ruling rather than a clean defeat."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A genuine legal surprise — a unanimous defeat for the government after lower courts had split. "
            "Telegraph, Times and Sky News leaned toward a government win or non-justiciability (FALSE); Guardian read the challenge as likely to succeed (TRUE); BBC/Reuters hedged (PARTIAL)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Government Faces Real Risk of Defeat as Supreme Court Weighs Prorogation",
                "article_date": "2019-09-20",
                "article_summary": (
                    "The Guardian reports that the government faces a real risk of defeat at the Supreme Court, arguing that the Scottish Court of Session's finding of unlawfulness and the justices' pointed questioning suggest the challenge may succeed. "
                    "The paper frames the prorogation as vulnerable to a ruling that it was an improper attempt to silence Parliament. "
                    "The Guardian judges that the court is likely to find against the government."
                ),
                "framing_prediction": "GOV_WILL_LOSE",
                "source_correct": "TRUE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Prorogation Case: Supreme Court Ruling Could Go Either Way, Lawyers Say",
                "article_date": "2019-09-20",
                "article_summary": (
                    "The BBC reports that legal commentators are divided on the prorogation case, with the split between the English and Scottish courts making the Supreme Court's ruling genuinely hard to predict. "
                    "Its correspondents note the central question of whether the matter is justiciable at all. "
                    "The BBC frames the outcome as uncertain and declines to forecast it."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Government Confident Court Will Rule Prorogation a Matter for Politics, Not Judges",
                "article_date": "2019-09-20",
                "article_summary": (
                    "The Telegraph reports that government lawyers are confident the Supreme Court will accept that prorogation is an inherently political act beyond judicial reach, echoing the English High Court's finding. "
                    "The paper frames any judicial intervention as constitutional overreach unlikely to command the court. "
                    "The Telegraph predicts the government will win the case."
                ),
                "framing_prediction": "GOV_WILL_WIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Judges Expected to Side With Government on Non-justiciability of Prorogation",
                "article_date": "2019-09-20",
                "article_summary": (
                    "The Times reports that several constitutional lawyers expect the Supreme Court to side with the government on the ground that prorogation is a political matter the courts should not adjudicate. "
                    "The paper notes the English High Court's earlier ruling in the government's favour as a strong indicator. "
                    "The Times predicts a government win."
                ),
                "framing_prediction": "GOV_WILL_WIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Supreme Court to Rule on Legality of Johnson's Parliament Suspension",
                "article_date": "2019-09-20",
                "article_summary": (
                    "Reuters reports that the Supreme Court will rule on whether Boris Johnson's suspension of Parliament was lawful, in a case with major constitutional implications. "
                    "The wire service notes the conflicting lower-court rulings and the uncertainty over whether the issue is justiciable, without projecting an outcome. "
                    "Reuters makes no forecast."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Government Tipped to Win Prorogation Case on Justiciability Argument",
                "article_date": "2019-09-20",
                "article_summary": (
                    "Sky News reports that several legal analysts tip the government to prevail in the prorogation case, expecting the Supreme Court to be reluctant to intervene in what ministers cast as a political decision. "
                    "Sky's coverage frames a clean defeat for the government as the less likely scenario given the divided lower courts. "
                    "Sky predicts a government win."
                ),
                "framing_prediction": "GOV_WILL_WIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 45 — Dominic Cummings Barnard Castle May 2020: Survives Calls to Go
    # -----------------------------------------------------------------------
    {
        "event_id": 45,
        "event_name": "Dominic Cummings Barnard Castle May 2020 – Survives",
        "event_date": "2020-05-25",
        "initial_coverage_date": "2020-05-23",
        "resolution_time_hours": 48,
        "event_category": "Scandal",
        "outcome": "Dominic Cummings did not resign and was not sacked over his lockdown trip to Durham and Barnard Castle; Boris Johnson publicly backed him and Cummings gave a defiant statement, surviving the crisis.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "Reports that the Prime Minister's chief adviser Dominic Cummings travelled from London to Durham during lockdown — and made a further trip to Barnard Castle — have provoked widespread public anger and accusations of double standards. "
            "Opposition parties, much of the press and a growing number of Conservative MPs are calling for Cummings to resign or be sacked. "
            "With Downing Street initially silent on his future and the political pressure intensifying, much commentary anticipates that Cummings will have to go."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A scandal where intense resignation pressure did NOT produce a departure. Guardian, Times and Sky News framed Cummings's position as untenable (FALSE); "
            "Telegraph judged Johnson would stand by him (TRUE); BBC/Reuters hedged (PARTIAL)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Cummings's Position Looks Untenable as Pressure to Resign Mounts",
                "article_date": "2020-05-23",
                "article_summary": (
                    "The Guardian reports that Dominic Cummings's position looks untenable as anger over his lockdown travel spreads across the public, the opposition and Conservative backbenches. "
                    "The paper argues that the perceived hypocrisy strikes at the heart of the government's public-health messaging and that few advisers survive such sustained pressure. "
                    "The Guardian frames Cummings's resignation or sacking as the likely outcome."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Dominic Cummings: Pressure Grows but No 10 Stands Firm for Now",
                "article_date": "2020-05-23",
                "article_summary": (
                    "The BBC reports that pressure is growing on Dominic Cummings over his lockdown trip, but that Downing Street is so far standing firm and declining to discuss his future. "
                    "Its correspondents note the rising number of Conservative MPs voicing concern while cautioning that the Prime Minister's backing could prove decisive. "
                    "The BBC declines to forecast whether Cummings will go."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Johnson Set to Stand by Cummings Despite Storm Over Lockdown Trip",
                "article_date": "2020-05-23",
                "article_summary": (
                    "The Telegraph reports that Boris Johnson is set to stand by Dominic Cummings despite the storm over his lockdown travel, viewing his chief adviser as indispensable to the government's agenda. "
                    "The paper frames the controversy as a media and opposition campaign the Prime Minister intends to ride out. "
                    "The Telegraph predicts Cummings will survive."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Cummings Urged to Consider His Position as Tory MPs Break Cover",
                "article_date": "2020-05-23",
                "article_summary": (
                    "The Times reports that a growing number of Conservative MPs are breaking cover to urge Dominic Cummings to consider his position, with the paper's own analysis suggesting his continued presence is a liability. "
                    "Coverage frames the scale of the backlash as difficult for any adviser to withstand. "
                    "The Times judges that Cummings is likely to have to step down."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK PM's Aide Cummings Under Pressure Over Lockdown Travel",
                "article_date": "2020-05-23",
                "article_summary": (
                    "Reuters reports that Boris Johnson's chief adviser Dominic Cummings is under intense pressure over reports he travelled during the coronavirus lockdown. "
                    "The wire service sets out the allegations and the calls for his resignation while noting Downing Street has not indicated he will go. "
                    "Reuters makes no forecast of the outcome."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Cummings's Future in Serious Doubt as Backlash Intensifies",
                "article_date": "2020-05-23",
                "article_summary": (
                    "Sky News reports that Dominic Cummings's future is in serious doubt as the backlash over his lockdown trip intensifies among the public and Conservative MPs. "
                    "Sky's political team frames the controversy as the kind of sustained pressure that typically forces an adviser out. "
                    "Sky suggests Cummings is unlikely to survive."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 46 — Priti Patel Bullying Finding November 2020: Survives Despite Breach
    # -----------------------------------------------------------------------
    {
        "event_id": 46,
        "event_name": "Priti Patel Bullying Finding November 2020 – Survives",
        "event_date": "2020-11-20",
        "initial_coverage_date": "2020-11-18",
        "resolution_time_hours": 60,
        "event_category": "Scandal",
        "outcome": "Despite the independent adviser finding that Priti Patel had breached the ministerial code through bullying behaviour, Boris Johnson backed her and she remained Home Secretary; the adviser, Sir Alex Allan, resigned instead.",
        "outcome_binary": "SURVIVED",
        "event_description": (
            "The independent adviser on ministerial standards, Sir Alex Allan, has concluded an inquiry into allegations that Home Secretary Priti Patel bullied civil servants. "
            "Reports indicate the findings are critical and may amount to a breach of the ministerial code, which by convention can end a minister's career. "
            "With the inquiry's conclusions imminent and the convention that code breaches lead to resignation, much commentary anticipates that Patel will have to step down or be removed."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A scandal where an adverse ethics finding did NOT end the minister's career. Guardian, Times and Sky News expected Patel to go (FALSE); "
            "Telegraph judged Johnson would protect her (TRUE); BBC/Reuters hedged (PARTIAL)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Patel Faces Calls to Resign as Bullying Inquiry Finds Against Her",
                "article_date": "2020-11-18",
                "article_summary": (
                    "The Guardian reports that Priti Patel faces mounting calls to resign as the independent adviser's inquiry is expected to find she breached the ministerial code through bullying. "
                    "The paper notes the long-standing convention that code breaches end ministerial careers and argues Patel's position will be hard to defend. "
                    "The Guardian frames her resignation or removal as the likely outcome."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Priti Patel: Ministerial Code Inquiry Findings Expected Imminently",
                "article_date": "2020-11-18",
                "article_summary": (
                    "The BBC reports that the findings of the inquiry into bullying allegations against Priti Patel are expected imminently, with the central question being whether she breached the ministerial code. "
                    "Its correspondents note the convention around code breaches while cautioning that the final decision rests with the Prime Minister. "
                    "The BBC declines to forecast Patel's fate."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "Johnson Expected to Stand by Patel Even if Inquiry Is Critical",
                "article_date": "2020-11-18",
                "article_summary": (
                    "The Telegraph reports that Boris Johnson is expected to stand by Priti Patel even if the inquiry is critical, with allies framing the allegations as a mischaracterisation of a demanding but legitimate management style. "
                    "The paper notes the Prime Minister's reluctance to lose a prominent Home Secretary to what supporters call a Whitehall campaign. "
                    "The Telegraph predicts Patel will survive."
                ),
                "framing_prediction": "WILL_SURVIVE",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Patel's Position in Doubt as Code-breach Finding Looms",
                "article_date": "2020-11-18",
                "article_summary": (
                    "The Times reports that Priti Patel's position is in doubt as a finding that she breached the ministerial code looms, with the paper's analysis noting that such findings have historically forced ministers out. "
                    "Coverage frames the imminent report as a serious threat to her tenure as Home Secretary. "
                    "The Times judges that Patel is likely to have to resign."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK Home Secretary Patel Awaits Findings of Bullying Inquiry",
                "article_date": "2020-11-18",
                "article_summary": (
                    "Reuters reports that Home Secretary Priti Patel awaits the findings of an independent inquiry into allegations that she bullied civil servants. "
                    "The wire service sets out the allegations and the ministerial-code context without projecting whether she will keep her job. "
                    "Reuters makes no forecast."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Pressure Mounts on Patel to Quit as Bullying Findings Near",
                "article_date": "2020-11-18",
                "article_summary": (
                    "Sky News reports that pressure is mounting on Priti Patel to quit as the bullying inquiry nears its conclusion, with its analysts noting the convention that ministerial-code breaches end careers. "
                    "Sky's coverage frames an adverse finding as likely to make her position untenable. "
                    "Sky suggests Patel is likely to have to step down."
                ),
                "framing_prediction": "WILL_RESIGN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
    # -----------------------------------------------------------------------
    # EVENT 47 — Uxbridge & South Ruislip By-election July 2023: Conservative Hold
    # -----------------------------------------------------------------------
    {
        "event_id": 47,
        "event_name": "Uxbridge & South Ruislip By-election July 2023 – Conservative Hold",
        "event_date": "2023-07-20",
        "initial_coverage_date": "2023-07-17",
        "resolution_time_hours": 72,
        "event_category": "Election_Leadership",
        "outcome": "The Conservatives narrowly held Uxbridge & South Ruislip by around 500 votes, defying widespread expectations of a Labour gain, with the planned expansion of the ULEZ charging zone widely credited for the result.",
        "outcome_binary": "CON_HOLD",
        "event_description": (
            "The by-election in Boris Johnson's former seat takes place with Labour holding a commanding national poll lead and the Conservatives braced for heavy by-election losses. "
            "Most analyses expect Labour to gain Uxbridge & South Ruislip comfortably as part of a strong night for the opposition. "
            "A local controversy over the expansion of London's Ultra Low Emission Zone (ULEZ) is bubbling, but its electoral impact is widely underestimated in pre-election coverage."
        ),
        "outcome_confirmed_by": "BBC News",
        "experimental_plan_note": (
            "A surprise Conservative hold against the expected Labour gain, driven by a local ULEZ backlash. "
            "Guardian, Times and Sky News expected a Labour gain (FALSE); Telegraph sensed ULEZ rescuing the Conservatives (TRUE); BBC/Reuters hedged (PARTIAL)."
        ),
        "sources": [
            {
                "source_name": "Guardian",
                "article_headline": "Labour on Course to Take Uxbridge as Tory Vote Crumbles",
                "article_date": "2023-07-17",
                "article_summary": (
                    "The Guardian reports that Labour is on course to take Uxbridge & South Ruislip, with the party's commanding national lead and the Conservatives' difficulties pointing to a gain in Boris Johnson's former seat. "
                    "The paper notes local unease about the ULEZ expansion but judges it unlikely to outweigh the national swing to Labour. "
                    "The Guardian frames a Labour gain as the most probable outcome."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
            {
                "source_name": "BBC",
                "article_headline": "Uxbridge By-election: Labour Hopes to Gain Johnson's Former Seat",
                "article_date": "2023-07-17",
                "article_summary": (
                    "The BBC reports that Labour hopes to gain Uxbridge & South Ruislip in a strong expected night of by-elections, while local controversy over the ULEZ expansion adds an unpredictable element. "
                    "Its analysts note the national picture favours Labour but caution that the ULEZ issue could complicate the result. "
                    "The BBC declines to forecast a winner."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Telegraph",
                "article_headline": "ULEZ Backlash Could Save the Tories in Uxbridge, Strategists Believe",
                "article_date": "2023-07-17",
                "article_summary": (
                    "The Telegraph reports that Conservative strategists believe a local backlash against the ULEZ expansion could save the party in Uxbridge & South Ruislip, turning the by-election into a referendum on the charging zone. "
                    "The paper frames the ULEZ issue as cutting through more powerfully than the national polls suggest. "
                    "The Telegraph predicts the Conservatives may hold the seat against expectations."
                ),
                "framing_prediction": "WILL_HOLD",
                "source_correct": "TRUE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Times",
                "article_headline": "Labour Favourite to Capture Uxbridge in Blow to Sunak",
                "article_date": "2023-07-17",
                "article_summary": (
                    "The Times reports that Labour is the clear favourite to capture Uxbridge & South Ruislip, in what would be a symbolic blow to Rishi Sunak as the party takes Boris Johnson's old seat. "
                    "The paper notes the ULEZ row but judges the national swing decisive. "
                    "The Times predicts a Labour gain."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "PAYWALLED",
            },
            {
                "source_name": "Reuters",
                "article_headline": "UK's Labour Eyes By-election Gains as Conservatives Brace for Losses",
                "article_date": "2023-07-17",
                "article_summary": (
                    "Reuters reports that Labour is eyeing gains in a set of by-elections, including Uxbridge & South Ruislip, as the Conservatives brace for losses amid a large national polling deficit. "
                    "The wire service notes the local ULEZ controversy as a wildcard without projecting the result. "
                    "Reuters makes no forecast."
                ),
                "framing_prediction": "UNCLEAR",
                "source_correct": "PARTIAL",
                "paywall_note": "FREE",
            },
            {
                "source_name": "Sky News",
                "article_headline": "Labour Set to Gain Uxbridge as Part of Strong By-election Night",
                "article_date": "2023-07-17",
                "article_summary": (
                    "Sky News reports that Labour is set to gain Uxbridge & South Ruislip as part of an expected strong by-election night, with its analysts citing the national polling lead and Conservative unpopularity. "
                    "Sky's coverage frames the ULEZ row as a local irritant unlikely to prevent a Labour win. "
                    "Sky predicts a Labour gain."
                ),
                "framing_prediction": "WILL_GAIN",
                "source_correct": "FALSE",
                "paywall_note": "FREE",
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def flatten_events(events: list) -> list:
    """Return one dict per source per event (long format) for CSV export."""
    rows = []
    for event in events:
        base = {k: v for k, v in event.items() if k != "sources"}
        for source in event["sources"]:
            rows.append({**base, **source})
    return rows


def save_csv(output_path: str = "uk_political_events.csv") -> None:
    rows = flatten_events(EVENTS)
    if not rows:
        print("No data.")
        return
    fieldnames = list(rows[0].keys())
    path = Path(output_path)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows ({len(EVENTS)} events × 6 sources) -> {path.resolve()}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "uk_political_events.csv"
    save_csv(out)
