#!/usr/bin/env bash
# John Hurst
# 2024-04-25

mode=$1 # 'sampler' or 'estimator'

if [ "$mode" != "sampler" ] && [ "$mode" != "estimator" ]; then
    echo "Invalid mode: $mode, must be 'sampler' or 'estimator'"
    exit 1
fi

bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=basic_simulator   > basic_simulator_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_algiers      > fake_algiers_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_almaden      > fake_almaden_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_armonk       > fake_armonk_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_athens       > fake_athens_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_auckland     > fake_auckland_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_belem        > fake_belem_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_boeblingen   > fake_boeblingen_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_bogota       > fake_bogota_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_brisbane     > fake_brisbane_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_brooklyn     > fake_brooklyn_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_burlington   > fake_burlington_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_cairo        > fake_cairo_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_cambridge    > fake_cambridge_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_casablanca   > fake_casablanca_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_cusco        > fake_cusco_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_essex        > fake_essex_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_geneva       > fake_geneva_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_guadalupe    > fake_guadalupe_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_hanoi        > fake_hanoi_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_jakarta      > fake_jakarta_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_johannesburg > fake_johannesburg_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_kawasaki     > fake_kawasaki_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_kolkata      > fake_kolkata_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_kyiv         > fake_kyiv_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_kyoto        > fake_kyoto_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_lagos        > fake_lagos_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_lima         > fake_lima_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_london       > fake_london_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_manhattan    > fake_manhattan_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_manila       > fake_manila_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_melbourne    > fake_melbourne_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_montreal     > fake_montreal_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_mumbai       > fake_mumbai_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_nairobi      > fake_nairobi_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_osaka        > fake_osaka_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_oslo         > fake_oslo_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_ourense      > fake_ourense_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_paris        > fake_paris_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_peekskill    > fake_peekskill_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_perth        > fake_perth_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_prague       > fake_prague_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_poughkeepsie > fake_poughkeepsie_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_quebec       > fake_quebec_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_quito        > fake_quito_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_rochester    > fake_rochester_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_rome         > fake_rome_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_santiago     > fake_santiago_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_sherbrooke   > fake_sherbrooke_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_singapore    > fake_singapore_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_sydney       > fake_sydney_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_torino       > fake_torino_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_toronto      > fake_toronto_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_valencia     > fake_valencia_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_vigo         > fake_vigo_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_washington   > fake_washington_${mode}.csv
bin/homework12_q2_qiskit_fakenoise_${mode}.py --runs=100 --provider=fake_yorktown     > fake_yorktown_${mode}.csv
