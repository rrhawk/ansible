# Working with Secrets

# 1. Encrypting/Decrypting Secrets with Ansible-Vault

## Documentation:
- https://docs.ansible.com/ansible/latest/user_guide/vault.html

### 1.1 Decrypting Secrets

Using password file `./passwords` decrypt following values and fill the table below:

<details><summary>spoiler1:</summary>

```yaml
!vault |
          $ANSIBLE_VAULT;1.2;AES256;dev
          31313936326634633831353534346166313065616165396666313061303561626337666637653738
          3761643932326637386163636136613734636131653635350a613733393364643135623332393762
          37616538346461656439363135323234366561626166643335383139323063346262303861633833
          3238343265343030620a323733336336616631623635623432643633383664626561366561323761
          64653333356561303232376430336437363564303538663663616562383933346631
```
</details>

<details><summary>spoiler2:</summary>

```yaml
!vault |
          $ANSIBLE_VAULT;1.2;AES256;test
          64616133323133323266386235306531356264656161386131633038343166636134643066623730
          3466306232653635363332383035353639633537356433640a633135653165613935363339333434
          38373931336131346566326264353165323162326430396562373332336431303038373033333362
          6237303531306639360a326461383639633330633839306564663435323164303930363334646465
          6437
```
</details>

<details><summary>spoiler3:</summary>

```yaml
!vault |
          $ANSIBLE_VAULT;1.2;AES256;stage
          34643666333634663334343465616366653539363037363762333834393935303162303461353331
          3730363833623666336231376133323965616430383635610a383031353362393662613430613834
          33623333663265633563643865313437636261343634636462326536393564636661323039623734
          3933366263666464380a363161396335666132373564643532376136646630326261356132313235
          6138
```
</details>

<details><summary>spoiler4:</summary>

```yaml
!vault |
          $ANSIBLE_VAULT;1.2;AES256;prod
          62323732623234303236343831396263363532386133623133366665663837656336313963366333
          3936313035396634336565373736356161663735653233360a363665303530356661313138613934
          63636361353036396162643266613632363737386162313932666335323662393531393639646130
          3136326132383062370a626631613031306565366631396331646533613466356539666366346336
          62666136323766636237633061326635613761313234643434313135316463336134
```
</details>

#### Result:

| Secret Name | Decrypted Value |
| --- | --- |
| spoiler1 | That is mutual! |
| spoiler2 | I love Belarus. |
| spoiler3 | That is mutual! |
| spoiler4 | Long live Belarus! |

### 1.2 Encrypting Secrets

Using password file `./passwords` encrypt several values:

Secrets to be encrypted:

- secret1: `Password12345`, vault-id: `dev`
- secret2: `Password3456`, vault-id: `test`
- secret3: `phul3AiFai0Ebei5`, vault-id: `stage`
- secret4: `kah7ahLu Eed1ohch Sa0hoh1W`, vault-id: `prod`

Create playbook - `using-encrypted-secrets.yml` and print out decrypted values with `debug` module:

```yaml
tasks:
  - debug: var=secret1
  - debug: var=secret2
  - debug: var=secret3
  - debug: var=secret4
```