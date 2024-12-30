FROM softwaresecurityproject/zap-stable:2.15.0

COPY ./zap/policies/ /home/zap/.ZAP/policies/

RUN ./zap.sh -addoninstallall -cmd
RUN ./zap.sh -addonuninstall communityScripts -cmd
RUN ./zap.sh -addonuninstall wappalyzer -cmd

