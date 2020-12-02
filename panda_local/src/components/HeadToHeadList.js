import React from 'react';
import react from 'react';
import styles from "./HeadToHeadList.module.css";
const HeadToHeadList = (props) => {
  const { repos } = props;
  if (!repos || repos.length === 0) return <p>No Tournaments entered by that player, sorry</p>;
  return (
      <div>
  <p>Set Count: {repos[1][repos[0]["player1"]]} - {repos[1][repos[0]["player2"]]} ({100 * repos[1][repos[0]["player1"]] / (repos[1][repos[0]["player1"]] + repos[1][repos[0]["player2"]])})%</p>
  <p>Game Count: {repos[2][repos[0]["player1"]]} - {repos[2][repos[0]["player2"]]} ({100 * repos[2][repos[0]["player1"]] / (repos[2][repos[0]["player1"]] + repos[2][repos[0]["player2"]])})%</p>
      <table>
        <tr>
            <th>{repos[0]["player1"]} Placement</th>
            <th>Tournament Name</th> 
            <th>{repos[0]["player2"]} Placement</th>
        </tr>
      
        {repos.splice(4).map((repo) => {
            return (
            <tr key={repo.id} className='list'>
                <td >{repo.placings[0]}</td>
                <td >{repo.tournament} </td>
                <td >{repo.placings[1]}</td>
            </tr>
            );
        })}
      </table>

      <table>
        <tr>
            <th>{repos[0]["player1"]} Set Score</th>
            <th>Tournament Name</th> 
            <th>Round</th> 
            <th>{repos[0]["player2"]} Set Score</th>
        </tr>
      
        {(repos[3]).map((repo) => {
            return (
            <tr key={repo.id} className='list'>
                <td >{repo.player1}</td>
                <td >{repo.Tournament} </td>
                <td >{repo.Round}</td>
                <td >{repo.player2}</td>
            </tr>
            );
        })}
      </table>
      </div>
    // <ul>
    //   <h2 className='list-head'>Tournament Placings by that Player</h2>
    //   {repos.map((repo) => {
    //     return (
    //       <li key={repo.id} className='list'>
    //         <span className={styles.span}>{repo.placings[0]}</span>
    //         <span className={styles.span}>{repo.tournament} </span>
    //         <span className={styles.span}>{repo.placings[1]}</span>
    //       </li>
    //     );
    //   })}
    // </ul>
  );
};
export default HeadToHeadList;