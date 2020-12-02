import React from 'react';
import react from 'react';
import styles from "./HeadToHeadList.module.css";
const EloList = (props) => {
  const { repos } = props;
  if (!repos || repos.length === 0) return <p>No Tournaments entered by that player, sorry</p>;
  return (
      <table className ={styles.table} key="Elo table">
        <thead>
        <tr>
            <th className ={styles.th}>Player</th>
            <th className ={styles.th}>Ranking</th> 
        </tr>
        </thead>
        <tbody>
        {repos.map((repo, i) => {
            return (
            <tr key={i} className='list'>
                <td key={i} className ={styles.td}>{repo.Player}</td>
                <td key={-i} className ={styles.td}>{repo.Elo} </td>
            </tr>
            );
        })}
        </tbody>
      </table>
  );
};
export default EloList;