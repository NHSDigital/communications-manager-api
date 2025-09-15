FROM softwaresecurityproject/zap-stable:2.16.1

COPY ./zap/policies/ /home/zap/.ZAP/policies/

RUN ./zap.sh -addoninstallall -cmd \
  && ./zap.sh -addonuninstall communityScripts -cmd \
  && ./zap.sh -addonuninstall packpentester -cmd \
  && ./zap.sh -addonuninstall wappalyzer -cmd
