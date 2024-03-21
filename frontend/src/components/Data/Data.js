import React, { useState } from 'react';
import axios from 'axios';
import './Data.css';

function Data() {
  return (
    <div style={{textAlign: 'center', padding: '20px'}}>
      <h1>What NFL data would you like to include in your model?</h1>
      <p>Select the statistics you would like to use to train your model</p>

      <div class='grid-container'>

        <div class='general'>
            <h2>General</h2>
        </div>

        <div class='general-grid-container'>
            <button class='h2h'>Head-to-Head Winner</button>
            <button class='homeID'>Home Team ID</button>
            <button class='awayID'>Away Team ID</button>
        </div>

        <div class='player'>
            <h2>Player</h2>
        </div>

        <div class='player-grid-container'>
            <button class='QB'>QB</button>
            <button class='RB'>RB</button>
            <button class='FB'>FB</button>
            <button class='WR'>FB</button>
            <button class='WR'>WR</button>
            <button class='TE'>TE</button>
            <button class='C'>C</button>
            <button class='G'>G</button>
            <button class='OT'>OT</button>
            <button class='DE'>DE</button>
            <button class='DT'>DT</button>
            <button class='CB'>CB</button>
            <button class='LB'>LB</button>
            <button class='S'>S</button>
            <button class='PK'>PK</button>
            <button class='P'>P</button>
            <button class='LS'>LS</button>
        </div>

        <div class='team'>
            <h2>Team</h2>
        </div>

        <div class='team-grid-container'>
            <button class='first_downs_total'>First Downs Total</button>
            <button class='first_downs_passing'>First Downs Passing</button>
            <button class='first_downs_rushing'>First Downs Rushing</button>    
            <button class='first_downs_from_penalties'>First Downs from Penalties</button>
            <button class='first_downs_third_down_efficiency'>First Downs Third Down Efficiency</button>
            <button class='first_downs_fourth_down_efficiency'>First Downs Fourth Down Efficiency</button>
            <button class='plays_total'>Plays Total</button>
            <button class='yards_total'>Yards Total</button>
            <button class='yards_yards_per_play'>Yards Per Play</button>
            <button class='yards_total_drives'>Yards Total Drives</button>
            <button class='passing_total'>Passing Total</button>
            <button class='passing_comp_att'>Passing Completions/Attempts</button>
            <button class='passing_yards_per_pass'>Passing Yards Per Pass</button>
            <button class='passing_interceptions_thrown'>Passing Interceptions Thrown</button>
            <button class='passing_sacks_yards_lost'>Passing Sacks/Yards Lost</button>
            <button class='rushings_total'>Rushings Total</button>
            <button class='rushings_attempts'>Rushings Attempts</button>
            <button class='rushings_yards_per_rush'>Rushings Yards Per Rush</button>
            <button class='red_zone_made_att'>Red Zone Made/Attempts</button>
            <button class='penalties_total'>Penalties Total</button>
            <button class='turnovers_total'>Turnovers Total</button>
            <button class='turnovers_lost_fumbles'>Turnovers Lost Fumbles</button>
            <button class='turnovers_interceptions'>Turnovers Interceptions</button>
            <button class='posession_total'>Posession Total</button>
            <button class='interceptions_total'>Interceptions Total</button>
            <button class='fumbles_recovered_total'>Fumbles Recovered Total</button>
            <button class='sacks_total'>Sacks Total</button>
            <button class='safeties_total'>Safeties Total</button>
            <button class='int_touchdowns_total'>Interception Touchdowns Total</button>
            <button class='points_against_total'>Points Against Total</button>
        </div>

      </div>

      <button className='continue-button'>Continue</button>

    </div>
  );
}

export default Data;