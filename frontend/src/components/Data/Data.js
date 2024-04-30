import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Data.css';

function Data() {

  const navigate = useNavigate();

  /* Default all data selections to true */
  const initialButtonStates = {
    h2h: true, homeID: true, awayID: true, QB: true, RB: true, FB: true,
    WR: true, TE: true, C: true, G: true, OT: true, DE: true, DT: true,
    CB: true, LB: true, S: true, PK: true, P: true, LS: true,
    first_downs_total: true, first_downs_passing: true, first_downs_rushing: true,
    first_downs_from_penalties: true, first_downs_third_down_efficiency: true,
    first_downs_fourth_down_efficiency: true, plays_total: true,
    yards_total: true, yards_yards_per_play: true, yards_total_drives: true,
    passing_total: true, passing_comp_att: true, passing_yards_per_pass: true,
    passing_interceptions_thrown: true, passing_sacks_yards_lost: true,
    rushings_total: true, rushings_attempts: true, rushings_yards_per_rush: true,
    red_zone_made_att: true, penalties_total: true, turnovers_total: true,
    turnovers_lost_fumbles: true, turnovers_interceptions: true,
    posession_total: true, interceptions_total: true, fumbles_recovered_total: true,
    sacks_total: true, safeties_total: true, int_touchdowns_total: true,
    points_against_total: true
  };
  const [clickedButtons, setClickedButtons] = useState(initialButtonStates);
  const [continueClicked, setContinueClicked] = useState(false);  // New state for tracking the "Continue" button click

  const handleButtonClick = (buttonName) => {
    setClickedButtons((prevState) => ({
      ...prevState,
      [buttonName]: !prevState[buttonName],
    }));
  };

  const handleContinue = () => {
    setContinueClicked(true);
    axios.post('http://localhost:5000/data', clickedButtons);
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>

      <div className="grid-container">
        <div className="general">
          <h2>General</h2>
        </div>

        <div className="general-grid-container">
          <button
            className={clickedButtons.h2h ? 'clicked' : 'h2h'}
            onClick={() => handleButtonClick('h2h')}
          >
            Head-to-Head Winner
          </button>

          <button
            className={clickedButtons.homeID ? 'clicked' : 'homeID'}
            onClick={() => handleButtonClick('homeID')}
          >
            Home Team ID
          </button>

          <button
            className={clickedButtons.awayID ? 'clicked' : 'awayID'}
            onClick={() => handleButtonClick('awayID')}
          >
            Away Team ID
          </button>
        </div>

        <div className="player">
          <h2>Player</h2>
        </div>

        <div className="player-grid-container">
          <button
            className={clickedButtons.QB ? 'clicked' : 'QB'}
            onClick={() => handleButtonClick('QB')}
          >
            QB
          </button>
          <button
            className={clickedButtons.RB ? 'clicked' : 'RB'}
            onClick={() => handleButtonClick('RB')}
          >
            RB
          </button>
          <button
            className={clickedButtons.FB ? 'clicked' : 'FB'}
            onClick={() => handleButtonClick('FB')}
          >
            FB
          </button>
          <button
            className={clickedButtons.WR ? 'clicked' : 'WR'}
            onClick={() => handleButtonClick('WR')}
          >
            WR
          </button>
          <button
            className={clickedButtons.TE ? 'clicked' : 'TE'}
            onClick={() => handleButtonClick('TE')}
          >
            TE
          </button>
          <button
            className={clickedButtons.C ? 'clicked' : 'C'}
            onClick={() => handleButtonClick('C')}
          >
            C
          </button>
          <button
            className={clickedButtons.G ? 'clicked' : 'G'}
            onClick={() => handleButtonClick('G')}
          >
            G
          </button>
          <button
            className={clickedButtons.OT ? 'clicked' : 'OT'}
            onClick={() => handleButtonClick('OT')}
          >
            OT
          </button>
          <button
            className={clickedButtons.DE ? 'clicked' : 'DE'}
            onClick={() => handleButtonClick('DE')}
          >
            DE
          </button>
          <button
            className={clickedButtons.DT ? 'clicked' : 'DT'}
            onClick={() => handleButtonClick('DT')}
          >
            DT
          </button>
          <button
            className={clickedButtons.CB ? 'clicked' : 'CB'}
            onClick={() => handleButtonClick('CB')}
          >
            CB
          </button>
          <button
            className={clickedButtons.LB ? 'clicked' : 'LB'}
            onClick={() => handleButtonClick('LB')}
          >
            LB
          </button>
          <button
            className={clickedButtons.S ? 'clicked' : 'S'}
            onClick={() => handleButtonClick('S')}
          >
            S
          </button>
          <button
            className={clickedButtons.PK ? 'clicked' : 'PK'}
            onClick={() => handleButtonClick('PK')}
          >
            PK
          </button>
          <button
            className={clickedButtons.P ? 'clicked' : 'P'}
            onClick={() => handleButtonClick('P')}
          >
            P
          </button>
          <button
            className={clickedButtons.LS ? 'clicked' : 'LS'}
            onClick={() => handleButtonClick('LS')}
          >
            LS
          </button>
        </div>

        <div className="team">
          <h2>Team</h2>
        </div>

        <div className="team-grid-container">
          <button
            className={clickedButtons.first_downs_total ? 'clicked' : 'first_downs_total'}
            onClick={() => handleButtonClick('first_downs_total')}
          >
            First Downs Total
          </button>
          <button
            className={clickedButtons.first_downs_passing ? 'clicked' : 'first_downs_passing'}
            onClick={() => handleButtonClick('first_downs_passing')}
          >
            First Downs Passing
          </button>
          <button
            className={clickedButtons.first_downs_rushing ? 'clicked' : 'first_downs_rushing'}
            onClick={() => handleButtonClick('first_downs_rushing')}
          >
            First Downs Rushing
          </button>
          <button
            className={clickedButtons.first_downs_from_penalties ? 'clicked' : 'first_downs_from_penalties'}
            onClick={() => handleButtonClick('first_downs_from_penalties')}
          >
            First Downs from Penalties
          </button>
          <button
            className={clickedButtons.first_downs_third_down_efficiency ? 'clicked' : 'first_downs_third_down_efficiency'}
            onClick={() => handleButtonClick('first_downs_third_down_efficiency')}
          >
            First Downs Third Down Efficiency
          </button>
          <button
            className={clickedButtons.first_downs_fourth_down_efficiency ? 'clicked' : 'first_downs_fourth_down_efficiency'}
            onClick={() => handleButtonClick('first_downs_fourth_down_efficiency')}
          >
            First Downs Fourth Down Efficiency
          </button>
          <button
            className={clickedButtons.plays_total ? 'clicked' : 'plays_total'}
            onClick={() => handleButtonClick('plays_total')}
          >
            Plays Total
          </button>
          <button
            className={clickedButtons.yards_total ? 'clicked' : 'yards_total'}
            onClick={() => handleButtonClick('yards_total')}
          >
            Yards Total
          </button>
          <button
            className={clickedButtons.yards_yards_per_play ? 'clicked' : 'yards_yards_per_play'}
            onClick={() => handleButtonClick('yards_yards_per_play')}
          >
            Yards Per Play
          </button>
          <button
            className={clickedButtons.yards_total_drives ? 'clicked' : 'yards_total_drives'}
            onClick={() => handleButtonClick('yards_total_drives')}
          >
            Yards Total Drives
          </button>
          <button
            className={clickedButtons.passing_total ? 'clicked' : 'passing_total'}
            onClick={() => handleButtonClick('passing_total')}
          >
            Passing Total
          </button>
          <button
            className={clickedButtons.passing_comp_att ? 'clicked' : 'passing_comp_att'}
            onClick={() => handleButtonClick('passing_comp_att')}
          >
            Passing Completions/Attempts
          </button>
          <button
            className={clickedButtons.passing_yards_per_pass ? 'clicked' : 'passing_yards_per_pass'}
            onClick={() => handleButtonClick('passing_yards_per_pass')}
          >
            Passing Yards Per Pass
          </button>
          <button
            className={clickedButtons.passing_interceptions_thrown ? 'clicked' : 'passing_interceptions_thrown'}
            onClick={() => handleButtonClick('passing_interceptions_thrown')}
          >
            Passing Interceptions Thrown
          </button>
          <button
            className={clickedButtons.passing_sacks_yards_lost ? 'clicked' : 'passing_sacks_yards_lost'}
            onClick={() => handleButtonClick('passing_sacks_yards_lost')}
          >
            Passing Sacks/Yards Lost
          </button>
          <button
            className={clickedButtons.rushings_total ? 'clicked' : 'rushings_total'}
            onClick={() => handleButtonClick('rushings_total')}
          >
            Rushings Total
          </button>
          <button
            className={clickedButtons.rushings_attempts ? 'clicked' : 'rushings_attempts'}
            onClick={() => handleButtonClick('rushings_attempts')}
          >
            Rushings Attempts
          </button>
          <button
            className={clickedButtons.rushings_yards_per_rush ? 'clicked' : 'rushings_yards_per_rush'}
            onClick={() => handleButtonClick('rushings_yards_per_rush')}
          >
            Rushings Yards Per Rush
          </button>
          <button
            className={clickedButtons.red_zone_made_att ? 'clicked' : 'red_zone_made_att'}
            onClick={() => handleButtonClick('red_zone_made_att')}
          >
            Red Zone Made/Attempts
          </button>
          <button
            className={clickedButtons.penalties_total ? 'clicked' : 'penalties_total'}
            onClick={() => handleButtonClick('penalties_total')}
          >
            Penalties Total
          </button>
          <button
            className={clickedButtons.turnovers_total ? 'clicked' : 'turnovers_total'}
            onClick={() => handleButtonClick('turnovers_total')}
          >
            Turnovers Total
          </button>
          <button
            className={clickedButtons.turnovers_lost_fumbles ? 'clicked' : 'turnovers_lost_fumbles'}
            onClick={() => handleButtonClick('turnovers_lost_fumbles')}
          >
            Turnovers Lost Fumbles
          </button>
          <button
            className={clickedButtons.turnovers_interceptions ? 'clicked' : 'turnovers_interceptions'}
            onClick={() => handleButtonClick('turnovers_interceptions')}
          >
            Turnovers Interceptions
          </button>
          <button
            className={clickedButtons.posession_total ? 'clicked' : 'posession_total'}
            onClick={() => handleButtonClick('posession_total')}
          >
            Possession Total
          </button>
          <button
            className={clickedButtons.interceptions_total ? 'clicked' : 'interceptions_total'}
            onClick={() => handleButtonClick('interceptions_total')}
          >
            Interceptions Total
          </button>
          <button
            className={clickedButtons.fumbles_recovered_total ? 'clicked' : 'fumbles_recovered_total'}
            onClick={() => handleButtonClick('fumbles_recovered_total')}
          >
            Fumbles Recovered Total
          </button>
          <button
            className={clickedButtons.sacks_total ? 'clicked' : 'sacks_total'}
            onClick={() => handleButtonClick('sacks_total')}
          >
            Sacks Total
          </button>
          <button
            className={clickedButtons.safeties_total ? 'clicked' : 'safeties_total'}
            onClick={() => handleButtonClick('safeties_total')}
          >
            Safeties Total
          </button>
          <button
            className={clickedButtons.int_touchdowns_total ? 'clicked' : 'int_touchdowns_total'}
            onClick={() => handleButtonClick('int_touchdowns_total')}
          >
            Interception Touchdowns Total
          </button>
          <button
            className={clickedButtons.points_against_total ? 'clicked' : 'points_against_total'}
            onClick={() => handleButtonClick('points_against_total')}
          >
            Points Against Total
          </button>
        </div>
      </div>

      { <button className={`continue-button ${continueClicked ? 'clicked' : ''}`} onClick={handleContinue}>Confirm Selection</button> }
    </div>
  );
}

export default Data;