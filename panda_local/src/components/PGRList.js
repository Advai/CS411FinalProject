import React from 'react';
import react from 'react';
import styles from "./HeadToHeadList.module.css";
const PGRList = (props) => {
  const { resp } = props;
  if (!resp || resp.length === 0) return <p>No Tournaments entered by that player, sorry</p>;
  return (
      <table className ={styles.table} key="PGR table">
          <thead>
        <tr>
            <th className ={styles.th}>Player</th>
            <th className ={styles.th}>Ranking</th> 
        </tr>
        </thead>
        <tbody>
        {resp.map((repo, i) => {
            return (
            <tr key={repo.key} className='l'>
                <td key={repo.Player} className ={styles.td}>{repo.Player}</td>
                <td key={repo.Elo} className ={styles.td}>{repo.Elo} </td>
            </tr>
            );
        })}
        </tbody>
      </table>
  );
};
export default PGRList;