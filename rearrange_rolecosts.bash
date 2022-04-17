#!/bin/bash

set -e
set -o pipefail

fpm_price=''
declare -A main_roles=()

generate_role_costs() {
    echo $'\t\t''myRoleCosts'
    echo $'\t\t{'
    if [[ -n "$fpm_price" ]]
    then
        for role in ARMY ENGINEER ARMOR AIR FPM
        do
            echo $'\t\t\t'"RoleCost $role"
            echo $'\t\t\t{'
            echo $'\t\t\t\t'"myRole ${role}_ROLE"
            echo $'\t\t\t\t'"myPrice $fpm_price"
            if [[ "$role" = 'FPM' || -n "${main_roles["$role"]+_}" ]]
            then
                echo $'\t\t\t\t''myPriceType REBATE_UNIQUE'
            else
                echo $'\t\t\t\t''myPriceType REBATE_NORMAL'
            fi
            echo $'\t\t\t''}'
            echo
        done
    fi
    echo $'\t\t}'
    echo
}

capture_output=no
current_role=''
current_price=''
current_price_type=''
while IFS='' read -r line
do
    read -r token1 token2 <<<"$line"
    if [[ "$token1" = 'myRoleCosts' ]]
    then
        capture_output=yes
    elif [[ "$token1" = 'myRoleBlackList' ]]
    then
        generate_role_costs

        fpm_price=''
        main_roles=()
        capture_output=no
    fi

    if [[ "$capture_output" = no ]]
    then
        echo "$line"
        continue
    fi

    case "$token1" in
        'myRole') current_role="$token2";;
        'myPrice') current_price="$token2";;
        'myPriceType') current_price_type="$token2";;
        '}')
            if [[ "$current_role" = 'FPM_ROLE' ]]
            then
                fpm_price="$current_price"
            elif [[ "$current_price_type" = "REBATE_UNIQUE" || "$current_price_type" = "REBATE_REBATED" ]]
            then
                main_roles["${current_role%_ROLE}"]=''
            fi
            current_role=''
            current_price=''
            current_price_type=''
    esac
done < ModKit/units/unittypes_wic.juice
